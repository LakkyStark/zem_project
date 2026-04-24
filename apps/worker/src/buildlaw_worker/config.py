import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    s3_endpoint_url: str
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_bucket_name: str
    s3_region: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.environ["DATABASE_URL"],
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        s3_endpoint_url=os.environ.get("S3_ENDPOINT_URL", "http://127.0.0.1:9000"),
        s3_access_key_id=os.environ.get("S3_ACCESS_KEY_ID", "minioadmin"),
        s3_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY", "minioadmin"),
        s3_bucket_name=os.environ.get("S3_BUCKET_NAME", "buildlaw-documents"),
        s3_region=os.environ.get("S3_REGION", "us-east-1"),
    )

