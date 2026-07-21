"""DBN Standard schemas."""

from pydantic import BaseModel


class CriterionCreate(BaseModel):
    name: str
    description: str | None = None
    weight: float
    max_score: float
    sort_order: int = 0


class CriterionResponse(BaseModel):
    id: str
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
    id: str
    name: str
    description: str | None
    version: str
    is_active: bool
    criteria: list[CriterionResponse] = []

    model_config = {"from_attributes": True}
