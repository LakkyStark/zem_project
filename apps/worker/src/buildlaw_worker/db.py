import psycopg2
from psycopg2.extensions import connection as PgConnection

from buildlaw_worker.config import get_settings

def _normalize_dsn(url: str) -> str:
    return url.replace("postgresql+psycopg2://", "postgresql://", 1)


def get_connection() -> PgConnection:
    raw = get_settings().database_url
    dsn = _normalize_dsn(raw)
    if "supabase.co" in dsn and "sslmode=" not in dsn:
        return psycopg2.connect(dsn, sslmode="require")
    return psycopg2.connect(dsn)
