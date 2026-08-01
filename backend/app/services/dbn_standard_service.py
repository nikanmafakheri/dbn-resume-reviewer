"""DBN Standard service."""

from uuid import UUID

from app.core.database import Database
from app.domain.models.dbn_standard import DBNStandard
from app.repositories.dbn_standard_repo import DBNStandardRepository


class DBNStandardService:
    def __init__(self, standard_repo: DBNStandardRepository):
        self.standard_repo = standard_repo

    async def create_standard(
        self, name: str, version: str, description: str | None = None
    ) -> DBNStandard:
        standard = DBNStandard(
            name=name,
            version=version,
            description=description,
            created_by=UUID(Database.ANONYMOUS_USER_ID),
        )
        return await self.standard_repo.save(standard)
