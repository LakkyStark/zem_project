from __future__ import annotations

from dataclasses import dataclass

import boto3
from botocore.client import BaseClient

from buildlaw_worker.config import get_settings


@dataclass(frozen=True)
class StoredObject:
    data: bytes
    content_type: str | None


def _client() -> BaseClient:
    s = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=s.s3_endpoint_url,
        aws_access_key_id=s.s3_access_key_id,
        aws_secret_access_key=s.s3_secret_access_key,
        region_name=s.s3_region,
    )


def download(storage_key: str) -> StoredObject:
    s = get_settings()
    c = _client()
    resp = c.get_object(Bucket=s.s3_bucket_name, Key=storage_key)
    body = resp["Body"].read()
    ct = resp.get("ContentType")
    return StoredObject(data=body, content_type=ct)

