"""Alembic async migration environment."""

import asyncio
from logging.config import fileConfig
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import all models so Base.metadata is complete (must register before
# target_metadata is read below).
from app.domain.models import (
    analysis,  # noqa: F401
    dbn_standard,  # noqa: F401
    resume,  # noqa: F401
    user,  # noqa: F401
)
from app.domain.models.base import Base

# Alembic Config object
config = context.config

# Set up Python logging from the alembic.ini [loggers] section
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _migration_target() -> tuple[str, dict]:
    """Resolve the migration target (stripped URL + connect_args).

    Returns ``(url_without_params, connect_args)``. Neon connection strings
    carry ``?sslmode=require`` and may include ``channel_binding``. ``sslmode``
    maps to asyncpg's ``ssl`` connect_arg; ``channel_binding`` has no asyncpg
    equivalent (it's a psql/Neon URL option), so it is dropped — TLS is already
    required via ``sslmode=require``.
    """
    from app.core.config import settings

    url = str(settings.DATABASE_URL)
    connect_args: dict = {}
    param_to_connect_arg = {"sslmode": "ssl"}
    drop_params = {"channel_binding"}
    parts = urlsplit(url)
    params = parse_qs(parts.query)
    changed = False
    for name, arg in param_to_connect_arg.items():
        if name in params:
            connect_args[arg] = params.pop(name, ["require"])[0]
            changed = True
    for name in drop_params:
        if name in params:
            params.pop(name, None)
            changed = True
    if changed:
        query = urlencode({k: v[0] for k, v in params.items()}, doseq=True)
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))
    return url, connect_args


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (emit SQL without connecting)."""
    url, _ = _migration_target()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configure context and run migrations on a live connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations online."""
    configuration = config.get_section(config.config_ini_section, {})
    # Point at the resolved URL (settings DATABASE_URL, else alembic.ini), so
    # online migrations honor compose/CI Postgres overrides.
    url, connect_args = _migration_target()
    configuration["sqlalchemy.url"] = url
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
