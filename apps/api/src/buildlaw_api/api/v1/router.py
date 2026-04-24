from fastapi import APIRouter

from buildlaw_api.api.v1.routes import auth, documents, organizations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(documents.router, tags=["documents"])
