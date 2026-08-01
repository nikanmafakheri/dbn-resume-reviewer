"""ORM models package.

Re-exported so `from app.domain.models import Base` keeps working and so the
models register on Base.metadata when the package is imported.
"""

from app.domain.models.base import Base as Base
from app.domain.models.base import TimestampMixin as TimestampMixin
from app.domain.models.base import UUIDMixin as UUIDMixin
