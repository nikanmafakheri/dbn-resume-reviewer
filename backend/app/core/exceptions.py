"""Custom exception classes and FastAPI exception handlers."""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: str = "internal_error", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(message=detail, code="not_found", status_code=404)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(message=detail, code="unauthorized", status_code=401)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(message=detail, code="forbidden", status_code=403)


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(message=detail, code="conflict", status_code=409)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "code": exc.code},
    )


# Mapping to register on the app
exception_handlers: dict[int, type[AppException]] = {}  # populated in main.py
