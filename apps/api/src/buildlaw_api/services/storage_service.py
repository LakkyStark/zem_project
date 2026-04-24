import re
from urllib.parse import urlparse, urlunparse
from uuid import UUID

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
import httpx

from buildlaw_api.core.config import get_settings


def _s3_client() -> BaseClient:
    s = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=s.s3_endpoint_url or None,
        aws_access_key_id=s.s3_access_key_id,
        aws_secret_access_key=s.s3_secret_access_key,
        region_name=s.s3_region,
    )


def sanitize_filename(name: str) -> str:
    base = name.split("/")[-1] or "file"
    base = re.sub(r"[^a-zA-Z0-9._-]+", "_", base).strip("._") or "file"
    return base[:200]


def build_storage_key(organization_id: UUID, document_id: UUID, original_filename: str) -> str:
    safe = sanitize_filename(original_filename)
    return f"organizations/{organization_id}/documents/{document_id}/{safe}"


def _supabase_headers() -> dict[str, str]:
    s = get_settings()
    if not s.supabase_url or not s.supabase_service_role_key:
        raise RuntimeError("Supabase Storage не настроен")
    return {
        "apikey": s.supabase_service_role_key,
        "Authorization": f"Bearer {s.supabase_service_role_key}",
    }


def _supabase_bucket() -> str:
    return get_settings().supabase_storage_bucket


def upload_url(*, storage_key: str, mime_type: str, expires_in: int = 3600) -> str:
    """
    URL для загрузки файла (HTTP PUT).
    - Если задан SUPABASE_URL — signed upload URL Supabase Storage.
    - Иначе — S3 presigned PUT.
    """
    s = get_settings()
    if s.supabase_url:
        endpoint = (
            f"{s.supabase_url.rstrip('/')}/storage/v1/object/upload/sign/{_supabase_bucket()}/{storage_key}"
        )
        with httpx.Client(timeout=10.0) as client:
            r = client.post(
                endpoint,
                headers={**_supabase_headers(), "Content-Type": "application/json"},
                json={"expiresIn": int(expires_in)},
            )
            r.raise_for_status()
            data = r.json()
            signed = data.get("signedURL") or data.get("signedUrl") or data.get("signed_url")
            if not signed:
                raise RuntimeError("Supabase не вернул signedURL")
            return signed

    return presigned_put_url(storage_key=storage_key, mime_type=mime_type, expires_in=expires_in)


def presigned_put_url(*, storage_key: str, mime_type: str, expires_in: int = 3600) -> str:
    s = get_settings()
    client = _s3_client()
    url = client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": s.s3_bucket_name,
            "Key": storage_key,
            "ContentType": mime_type,
        },
        ExpiresIn=expires_in,
        HttpMethod="PUT",
    )
    public = s.s3_public_endpoint_url
    if public:
        pub = urlparse(public)
        cur = urlparse(url)
        url = urlunparse((pub.scheme, pub.netloc, cur.path, cur.params, cur.query, cur.fragment))
    return url


def head_object_exists(storage_key: str) -> bool:
    s = get_settings()
    if s.supabase_url:
        url = f"{s.supabase_url.rstrip('/')}/storage/v1/object/{_supabase_bucket()}/{storage_key}"
        with httpx.Client(timeout=10.0) as client:
            r = client.head(url, headers=_supabase_headers())
            if r.status_code == 200:
                return True
            if r.status_code == 404:
                return False
            r.raise_for_status()
            return False

    client = _s3_client()
    try:
        client.head_object(Bucket=s.s3_bucket_name, Key=storage_key)
        return True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            return False
        raise
