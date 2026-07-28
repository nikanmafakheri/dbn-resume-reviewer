"""API v1 router — aggregates all endpoint modules."""

from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .resumes import router as resumes_router
from .analysis import router as analysis_router
from .dbn_standard import router as dbn_standard_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(resumes_router, prefix="/resumes", tags=["resumes"])
router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
router.include_router(dbn_standard_router, prefix="/dbn-standards", tags=["dbn-standards"])
