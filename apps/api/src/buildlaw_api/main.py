from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from buildlaw_api.api.v1.router import api_router
from buildlaw_api.core.config import get_settings

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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.api_v1_prefix)
