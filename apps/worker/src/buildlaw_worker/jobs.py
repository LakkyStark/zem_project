"""Задачи RQ. Путь функции должен совпадать с тем, что ставит API в очередь."""

from __future__ import annotations

import logging
from uuid import UUID

from buildlaw_worker.db import get_connection
from buildlaw_worker.logging import setup_logging
from buildlaw_worker.ocr.mock import MockOcrProvider
from buildlaw_worker.storage import download

log = logging.getLogger(__name__)

def _ensure_pgcrypto(conn) -> None:
    # Needed for gen_random_uuid() used in inserts.
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    conn.commit()


def process_document(document_id: str) -> None:
    """
    Первый сквозной pipeline MVP:
    uploaded -> queued -> ocr_done/failed
    """
    setup_logging()
    doc_uuid = UUID(document_id)

    ocr = MockOcrProvider()

    conn = get_connection()
    try:
        _ensure_pgcrypto(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, organization_id, storage_key, original_filename, mime_type
                FROM documents
                WHERE id = %s::uuid
                """,
                (str(doc_uuid),),
            )
            row = cur.fetchone()
            if not row:
                log.warning("document not found", extra={"extra": {"document_id": document_id}})
                return

            _, organization_id, storage_key, original_filename, mime_type = row

            cur.execute(
                "UPDATE documents SET status = %s, error_message = NULL, updated_at = NOW() WHERE id = %s::uuid",
                ("queued", str(doc_uuid)),
            )
        conn.commit()

        obj = download(storage_key)
        pages = ocr.ocr(filename=original_filename, mime_type=mime_type, content=obj.data)

        with conn.cursor() as cur:
            # Idempotency-ish: wipe previous pages for re-runs
            cur.execute(
                "DELETE FROM document_pages WHERE organization_id = %s::uuid AND document_id = %s::uuid",
                (str(organization_id), str(doc_uuid)),
            )
            for p in pages:
                cur.execute(
                    """
                    INSERT INTO document_pages
                      (id, organization_id, document_id, page_number, ocr_text, confidence, provider)
                    VALUES
                      (gen_random_uuid(), %s::uuid, %s::uuid, %s, %s, %s, %s)
                    """,
                    (
                        str(organization_id),
                        str(doc_uuid),
                        p.page_number,
                        p.ocr_text,
                        float(p.confidence),
                        ocr.name,
                    ),
                )

            cur.execute(
                """
                UPDATE documents
                SET status = %s,
                    pages_count = %s,
                    updated_at = NOW()
                WHERE id = %s::uuid
                """,
                ("ocr_done", len(pages), str(doc_uuid)),
            )
        conn.commit()

        log.info(
            "document ocr done",
            extra={"extra": {"document_id": document_id, "pages_count": len(pages), "provider": ocr.name}},
        )
    except Exception as e:
        conn.rollback()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE documents
                    SET status = %s,
                        error_message = %s,
                        updated_at = NOW()
                    WHERE id = %s::uuid
                    """,
                    ("failed", str(e)[:2000], str(doc_uuid)),
                )
            conn.commit()
        except Exception:
            conn.rollback()
        log.exception("document processing failed", extra={"extra": {"document_id": document_id}})
        raise
    finally:
        conn.close()
