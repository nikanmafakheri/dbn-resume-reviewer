"""Periodic cleanup tasks — removes stale uploads and temp files."""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import select

from app.workers.celery import celery_app
from app.core.config import settings
from app.core.database import init_database, get_database
from app.domain.models.resume import Resume

logger = logging.getLogger(__name__)


@celery_app.task
def cleanup_stale_uploads():
    """Delete media files older than 24h with no linked resume record."""
    logger.info("Running stale upload cleanup")
    try:
        asyncio.run(_cleanup())
    except Exception as exc:
        logger.exception("Cleanup task failed: %s", exc)


async def _cleanup():
    """Async implementation of stale upload cleanup."""

    media_dir = settings.MEDIA_ROOT / "resumes"
    if not media_dir.exists():
        return

    init_database()
    db = get_database()

    async with db.session_factory() as session:
        result = await session.execute(select(Resume.file_path))
        known_paths = {row[0] for row in result.fetchall() if row[0]}

        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

        for fpath in media_dir.iterdir():
            if not fpath.is_file():
                continue
            if str(fpath) in known_paths:
                continue

            mtime = datetime.fromtimestamp(fpath.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                fpath.unlink(missing_ok=True)
                logger.info("Removed stale upload: %s", fpath.name)

    logger.info("Cleanup complete")
