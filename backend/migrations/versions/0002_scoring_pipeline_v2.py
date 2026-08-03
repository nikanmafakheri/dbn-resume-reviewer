"""Add scoring-pipeline-v2 columns: five-dimension scalars + nested scores_json.

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-02

Adds the columns that back the explainable five-dimension scoring system.
The legacy ``grammar_score`` / ``recruiter_score`` columns are intentionally
kept so historical analyses remain readable (additive, non-breaking change).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("analyses", sa.Column("skills_score", sa.Float(), nullable=True))
    op.add_column("analyses", sa.Column("experience_score", sa.Float(), nullable=True))
    op.add_column("analyses", sa.Column("formatting_score", sa.Float(), nullable=True))
    op.add_column("analyses", sa.Column("content_score", sa.Float(), nullable=True))
    op.add_column("analyses", sa.Column("summary_en", sa.Text(), nullable=True))
    op.add_column("analyses", sa.Column("analysis_fa", sa.Text(), nullable=True))
    op.add_column("analyses", sa.Column("scores_json", postgresql.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("analyses", "scores_json")
    op.drop_column("analyses", "analysis_fa")
    op.drop_column("analyses", "summary_en")
    op.drop_column("analyses", "content_score")
    op.drop_column("analyses", "formatting_score")
    op.drop_column("analyses", "experience_score")
    op.drop_column("analyses", "skills_score")
