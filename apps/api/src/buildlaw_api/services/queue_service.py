from uuid import UUID

from redis import Redis
from rq import Queue

from buildlaw_api.core.config import get_settings


def enqueue_process_document(document_id: UUID) -> None:
    settings = get_settings()
    conn = Redis.from_url(settings.redis_url)
    q = Queue("buildlaw_default", connection=conn)
    q.enqueue("buildlaw_worker.jobs.process_document", str(document_id))
