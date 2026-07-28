"""DBN Standard schemas."""

from uuid import UUID

from pydantic import BaseModel


class CriterionCreate(BaseModel):
    name: str
    description: str | None = None
    weight: float
    max_score: float
    sort_order: int = 0


class CriterionResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    weight: float
    max_score: float
    sort_order: int

    model_config = {"from_attributes": True}


class StandardCreate(BaseModel):
    name: str
    description: str | None = None
    version: str


class StandardResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    version: str
    is_active: bool
    criteria: list[CriterionResponse] = []

    model_config = {"from_attributes": True}
