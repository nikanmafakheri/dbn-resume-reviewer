"""Shared response schemas."""

from collections.abc import Sequence

from pydantic import BaseModel


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
