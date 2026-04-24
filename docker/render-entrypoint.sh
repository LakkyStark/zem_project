#!/usr/bin/env sh
set -eu

PORT="${PORT:-8000}"

echo "Running migrations..."
cd /app/apps/api
alembic upgrade head

echo "Starting RQ worker..."
rq worker buildlaw_default --url "${REDIS_URL}" &
WORKER_PID="$!"

echo "Starting API on :${PORT}..."
uvicorn buildlaw_api.main:app --host 0.0.0.0 --port "${PORT}" &
API_PID="$!"

term_handler() {
  echo "Stopping..."
  kill -TERM "${API_PID}" 2>/dev/null || true
  kill -TERM "${WORKER_PID}" 2>/dev/null || true
  wait "${API_PID}" 2>/dev/null || true
  wait "${WORKER_PID}" 2>/dev/null || true
}

trap term_handler INT TERM

wait "${API_PID}"
