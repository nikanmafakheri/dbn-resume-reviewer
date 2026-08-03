"""Assert the production index set is present on ORM metadata.

These indexes are the contract shipped by migration 0003. Keeping them in sync
between the ORM models and the migration matters: `Base.metadata.create_all`
(dev bootstrap) and `alembic upgrade head` (prod) must produce the same schema,
otherwise autogenerate drifts.
"""

# Import models so they register on Base.metadata.
import app.domain.models.analysis  # noqa: F401
import app.domain.models.dbn_standard  # noqa: F401
import app.domain.models.resume  # noqa: F401
import app.domain.models.user  # noqa: F401
from app.domain.models.base import Base


def _table_index_columns(table_name: str) -> dict[str, tuple[str, ...]]:
    table = next(t for t in Base.metadata.sorted_tables if t.name == table_name)
    return {
        idx.name: tuple(c.name for c in idx.columns)
        for idx in table.indexes
    }


def test_analyses_fk_and_listing_indexes():
    indexes = _table_index_columns("analyses")
    assert indexes["ix_analyses_resume_id"] == ("resume_id",)
    assert indexes["ix_analyses_user_id"] == ("user_id",)
    assert indexes["ix_analyses_dbn_standard_id"] == ("dbn_standard_id",)
    assert indexes["ix_analyses_status"] == ("status",)
    assert indexes["ix_analyses_created_at"] == ("created_at",)
    assert indexes["ix_analyses_resume_id_created_at"] == ("resume_id", "created_at")


def test_resumes_fk_and_listing_indexes():
    indexes = _table_index_columns("resumes")
    assert indexes["ix_resumes_user_id"] == ("user_id",)
    assert indexes["ix_resumes_status"] == ("status",)
    assert indexes["ix_resumes_created_at"] == ("created_at",)
    assert indexes["ix_resumes_user_id_status"] == ("user_id", "status")


def test_standard_criteria_and_standards_fk_indexes():
    assert _table_index_columns("dbn_standard_criteria")[
        "ix_dbn_standard_criteria_dbn_standard_id"
    ] == ("dbn_standard_id",)
    assert _table_index_columns("dbn_standards")["ix_dbn_standards_created_by"] == (
        "created_by",
    )


def test_users_role_index():
    assert _table_index_columns("users")["ix_users_role"] == ("role",)
