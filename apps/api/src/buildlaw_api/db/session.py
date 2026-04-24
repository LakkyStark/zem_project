from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from buildlaw_api.core.config import get_settings

settings = get_settings()
connect_args = {}
# Supabase Postgres требует SSL. Если sslmode не указан в URL — включаем require.
if "supabase.co" in settings.database_url and "sslmode=" not in settings.database_url:
    connect_args = {"sslmode": "require"}
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
