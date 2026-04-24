from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from buildlaw_api.api.v1.router import api_router
from buildlaw_api.core.config import get_settings
from buildlaw_api.db.session import engine

settings = get_settings()

app = FastAPI(
    title="BuildLaw AI API",
    description="REST API для BuildLaw AI (мультиарендность через organization_id).",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        # Если БД недоступна — это не "ok" для регистрации/логина.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database unavailable",
        )


app.include_router(api_router, prefix=settings.api_v1_prefix)
