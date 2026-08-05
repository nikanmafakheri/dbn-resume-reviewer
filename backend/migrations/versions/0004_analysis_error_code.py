"""Add analyses.error_code — structured failure classifier.

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-04

Pure additive change — no column/table drops, no data migration. Adds the
``error_code`` column used to distinguish a retryable quota/rate-limit pause
("rate_limited") from a genuine bug, so the frontend can render a friendly
"please wait" card instead of the raw provider error string.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "analyses",
        sa.Column("error_code", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("analyses", "error_code")
