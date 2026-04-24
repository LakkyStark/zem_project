import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    # S3/MinIO/R2 (optional)
    s3_endpoint_url: str | None
    s3_access_key_id: str | None
    s3_secret_access_key: str | None
    s3_bucket_name: str | None
    s3_region: str | None

    # Supabase Storage (optional)
    supabase_url: str | None
    supabase_service_role_key: str | None
    supabase_storage_bucket: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.environ["DATABASE_URL"],
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        s3_endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        s3_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
        s3_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        s3_bucket_name=os.environ.get("S3_BUCKET_NAME"),
        s3_region=os.environ.get("S3_REGION"),
        supabase_url=os.environ.get("SUPABASE_URL"),
        supabase_service_role_key=os.environ.get("SUPABASE_SERVICE_ROLE_KEY"),
        supabase_storage_bucket=os.environ.get("SUPABASE_STORAGE_BUCKET", "documents"),
    )

