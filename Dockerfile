FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip

# Copy monorepo apps needed for Render single-service deployment
COPY apps/api /app/apps/api
COPY apps/worker /app/apps/worker
COPY docker/render-entrypoint.sh /app/render-entrypoint.sh

RUN chmod +x /app/render-entrypoint.sh

# Install API and worker packages
RUN pip install --no-cache-dir -e /app/apps/api && pip install --no-cache-dir -e /app/apps/worker

EXPOSE 8000

CMD ["/app/render-entrypoint.sh"]

