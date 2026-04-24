#!/usr/bin/env sh
set -eu

echo "Waiting for DB..."
python - <<'PY'
import time
from sqlalchemy import create_engine, text
from buildlaw_api.core.config import get_settings

url = get_settings().database_url
engine = create_engine(url, pool_pre_ping=True, future=True)

for i in range(60):
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
        print("DB is ready")
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("DB not ready")
PY

echo "Running migrations..."
alembic upgrade head

echo "Starting API..."
PORT="${PORT:-8000}"
exec uvicorn buildlaw_api.main:app --host 0.0.0.0 --port "${PORT}"

