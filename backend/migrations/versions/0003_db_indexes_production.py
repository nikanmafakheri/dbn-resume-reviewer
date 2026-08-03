"""Add production indexes: FK lookups, listing order-by, composite filters.

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-03

Pure additive change — no column/table drops, no data migration. Adds the
indexes that make the common query patterns (join by FK, list newest-first,
filter by status, per-user/per-resume listing) fast on real row counts for
both SQLite and PostgreSQL.
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Foreign-key lookup indexes ────────────────────
    # SQLAlchemy does not auto-index FK columns; without these every JOIN and
    # every child→parent lookup is a sequential scan.
    op.create_index("ix_analyses_resume_id", "analyses", ["resume_id"])
    op.create_index("ix_analyses_user_id", "analyses", ["user_id"])
    op.create_index("ix_analyses_dbn_standard_id", "analyses", ["dbn_standard_id"])
    op.create_index("ix_resumes_user_id", "resumes", ["user_id"])
    op.create_index(
        "ix_dbn_standard_criteria_dbn_standard_id",
        "dbn_standard_criteria",
        ["dbn_standard_id"],
    )
    op.create_index("ix_dbn_standards_created_by", "dbn_standards", ["created_by"])

    # ── Listing / newest-first indexes ────────────────
    # list_all() orders by created_at desc in both resume and analysis repos.
    op.create_index("ix_resumes_created_at", "resumes", ["created_at"])
    op.create_index("ix_analyses_created_at", "analyses", ["created_at"])

    # ── Status / role filters ─────────────────────────
    op.create_index("ix_resumes_status", "resumes", ["status"])
    op.create_index("ix_analyses_status", "analyses", ["status"])
    op.create_index("ix_users_role", "users", ["role"])

    # ── Composite hot paths ───────────────────────────
    # resumes for a given user, filtered by status
    op.create_index("ix_resumes_user_id_status", "resumes", ["user_id", "status"])
    # analyses for a given resume, newest first
    op.create_index(
        "ix_analyses_resume_id_created_at", "analyses", ["resume_id", "created_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_analyses_resume_id_created_at", table_name="analyses")
    op.drop_index("ix_resumes_user_id_status", table_name="resumes")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_analyses_status", table_name="analyses")
    op.drop_index("ix_resumes_status", table_name="resumes")
    op.drop_index("ix_analyses_created_at", table_name="analyses")
    op.drop_index("ix_resumes_created_at", table_name="resumes")
    op.drop_index("ix_dbn_standards_created_by", table_name="dbn_standards")
    op.drop_index("ix_dbn_standard_criteria_dbn_standard_id", table_name="dbn_standard_criteria")
    op.drop_index("ix_resumes_user_id", table_name="resumes")
    op.drop_index("ix_analyses_dbn_standard_id", table_name="analyses")
    op.drop_index("ix_analyses_user_id", table_name="analyses")
    op.drop_index("ix_analyses_resume_id", table_name="analyses")
