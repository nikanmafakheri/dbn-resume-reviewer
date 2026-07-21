"""Scoring service — encapsulates DBN Standard interactions."""

from app.repositories.dbn_standard_repo import DBNStandardRepository


class ScoringService:
    def __init__(self, standard_repo: DBNStandardRepository):
        self.standard_repo = standard_repo

    async def get_active_standard(self):
        return await self.standard_repo.get_active()
