# BuildLaw AI — монорепозиторий MVP

AI SaaS для анализа строительных и земельно-правовых документов (скелет для развития OCR, извлечения данных, анализа и биллинга).

## Структура

```
├── apps/
│   ├── web/          # Next.js 15 (App Router) + TypeScript + Tailwind
│   ├── api/          # FastAPI + SQLAlchemy 2.0 + Alembic + Pydantic
│   └── worker/       # Python-воркер (Redis + RQ)
├── docker-compose.yml
└── README.md
```

Мультиарендность: все сущности с данными клиента привязаны к `organization_id` (кроме справочников `users` и `organizations`). Доступ к API проверяется через членство в организации (`memberships`).

## Требования

- Node.js 20+
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (рекомендуется) или `pip` + `venv`
- Docker и Docker Compose (PostgreSQL, Redis, MinIO)

## Быстрый старт (локально)

### 1. Инфраструктура

```bash
docker compose up -d postgres redis minio minio-init
```

### 2. API

```bash
cd apps/api
cp .env.example .env
uv venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
alembic upgrade head
uvicorn buildlaw_api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI: http://localhost:8000/docs  
- OpenAPI JSON: http://localhost:8000/openapi.json  

### 3. Worker

В отдельном терминале:

```bash
cd apps/worker
cp .env.example .env
uv venv && source .venv/bin/activate
uv pip install -e .
rq worker buildlaw_default --url redis://localhost:6379/0
```

### 4. Web

```bash
cd apps/web
cp .env.example .env.local
npm install
npm run dev
```

Приложение: http://localhost:3000  

## Переменные окружения

Скопируйте `.env.example` в каждом приложении (`apps/api`, `apps/worker`, `apps/web`). Секреты не коммитьте.

## Поток загрузки документа (presigned URL)

1. `POST /v1/organizations/{organization_id}/documents/upload-sessions` — создаётся запись `documents` со статусом `pending_upload`, возвращаются `document_id`, `upload_url`, `upload_fields` (для MinIO/S3).
2. Клиент выполняет `PUT` (или POST для browser form) на выданный URL с телом файла.
3. `POST /v1/organizations/{organization_id}/documents/{document_id}/complete-upload` — статус переводится в `uploaded`, в очередь Redis ставится задача на дальнейшую обработку (заглушка для OCR/анализа).

## Document flow (сквозной MVP)

1. Откройте web: `http://localhost:3000`, зарегистрируйтесь и перейдите в организацию.
2. Загрузите PDF на странице документов: создаётся upload session, затем файл уходит в MinIO по presigned PUT.
3. После `complete-upload` документ появляется в списке со статусом `uploaded`.
4. Воркер берёт задачу из Redis, выставляет `queued`, выполняет Mock OCR (best-effort извлечение текста из PDF), сохраняет `document_pages`, обновляет `pages_count`.
5. Статус становится `ocr_done`, в карточке документа показывается OCR preview по страницам. Если ошибка — `failed` + `error_message`.

## Тесты API

```bash
cd apps/api
source .venv/bin/activate
pytest -q
```

## Расширение домена

В `apps/api/src/buildlaw_api/domains/` зарезервированы каталоги `ocr`, `extraction`, `analysis`, `billing` — туда можно выносить сервисы и use-case без смешивания с HTTP-слоем.

## Deployment (рекомендуемая схема)

### Выбор платформ

- **Web (`apps/web`)**: Vercel
- **API + Worker + Postgres + Redis (`apps/api`, `apps/worker`)**: Railway (как 2 сервиса) + встроенные плагины Postgres/Redis
- **Object storage**: Cloudflare R2 или AWS S3

### Переменные окружения (prod)

**Vercel (web)**:
- `NEXT_PUBLIC_API_URL` = `https://<ваш-api-домен>` (Railway)

**Railway (api)**:
- `PORT` (Railway выставляет автоматически)
- `DATABASE_URL` (Railway Postgres)
- `REDIS_URL` (Railway Redis)
- `JWT_SECRET` (обязательно)
- `S3_BUCKET_NAME`
- `S3_REGION`
- `S3_ACCESS_KEY_ID`
- `S3_SECRET_ACCESS_KEY`
- `S3_ENDPOINT_URL` (для R2/MinIO; для AWS можно не задавать)
- `S3_PUBLIC_ENDPOINT_URL` (опционально; если presigned должны идти через кастомный домен)
- `CORS_ALLOW_ORIGINS` = `["https://<ваш-vercel-домен>"]`

**Railway (worker)**:
- `DATABASE_URL`
- `REDIS_URL`
- `S3_*` (как у api)

### Минимальный порядок деплоя

1. Создайте проект в Railway, добавьте плагины **Postgres** и **Redis**.
2. Задеплойте `apps/api` (Dockerfile уже есть). Проверьте `GET /health` и `GET /docs`.
3. Задеплойте `apps/worker` вторым сервисом (Dockerfile уже есть), подключите тот же `REDIS_URL` и `DATABASE_URL`.
4. Создайте bucket в R2/S3 и укажите `S3_*` переменные.
5. Задеплойте `apps/web` в Vercel, выставьте `NEXT_PUBLIC_API_URL` на домен API.

