"""Shared response schemas."""

from pydantic import BaseModel
from collections.abc import Sequence


class PaginatedResponse(BaseModel):
    items: Sequence
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    detail: str
    code: str
    errors: list[dict] = []
