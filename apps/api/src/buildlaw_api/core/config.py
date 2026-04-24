from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg2://buildlaw:buildlaw@localhost:5432/buildlaw"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # For AWS S3 you can omit endpoint_url (None). For MinIO/R2 set explicit endpoint.
    s3_endpoint_url: str | None = "http://127.0.0.1:9000"
    s3_public_endpoint_url: str | None = None
    s3_access_key_id: str = "minioadmin"
    s3_secret_access_key: str = "minioadmin"
    s3_bucket_name: str = "buildlaw-documents"
    s3_region: str = "us-east-1"

    api_v1_prefix: str = "/v1"
    cors_allow_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    # Supabase Storage (альтернатива S3/R2). Если задано SUPABASE_URL — используем Supabase.
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_storage_bucket: str = "documents"


@lru_cache
def get_settings() -> Settings:
    return Settings()
