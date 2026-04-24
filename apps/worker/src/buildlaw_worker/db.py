import psycopg2
from psycopg2.extensions import connection as PgConnection

from buildlaw_worker.config import get_settings

def _normalize_dsn(url: str) -> str:
    return url.replace("postgresql+psycopg2://", "postgresql://", 1)


def get_connection() -> PgConnection:
    raw = get_settings().database_url
    return psycopg2.connect(_normalize_dsn(raw))
