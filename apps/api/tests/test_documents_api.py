from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from buildlaw_api.models import Document, Organization
from buildlaw_api.models.enums import DocumentStatus


def test_list_documents_tenant_isolation(
    client, db_session: Session, seeded_orgs: dict[str, uuid.UUID]
) -> None:
    now = datetime.now(UTC)
    user_id = seeded_orgs["user"]
    org1 = seeded_orgs["org1"]
    org2 = seeded_orgs["org2"]

    # Create foreign org doc without membership: should never appear
    db_session.add_all(
        [
            Document(
                id=uuid.uuid4(),
                organization_id=org1,
                uploaded_by_id=user_id,
                storage_key="k1",
                type="egrn",
                original_filename="a.pdf",
                mime_type="application/pdf",
                size_bytes=10,
                pages_count=0,
                status=DocumentStatus.uploaded,
                created_at=now,
                updated_at=now,
            ),
            Document(
                id=uuid.uuid4(),
                organization_id=org2,
                uploaded_by_id=user_id,
                storage_key="k2",
                type="egrn",
                original_filename="b.pdf",
                mime_type="application/pdf",
                size_bytes=11,
                pages_count=0,
                status=DocumentStatus.uploaded,
                created_at=now,
                updated_at=now,
            ),
        ]
    )
    db_session.commit()

    r = client.get(f"/v1/organizations/{org1}/documents?limit=50")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["original_filename"] == "a.pdf"


def test_get_document_details_404_for_foreign_org(
    client, db_session: Session, seeded_orgs: dict[str, uuid.UUID]
) -> None:
    now = datetime.now(UTC)
    user_id = seeded_orgs["user"]
    org2 = seeded_orgs["org2"]

    doc = Document(
        id=uuid.uuid4(),
        organization_id=org2,
        uploaded_by_id=user_id,
        storage_key="k2",
        type="egrn",
        original_filename="b.pdf",
        mime_type="application/pdf",
        size_bytes=11,
        pages_count=0,
        status=DocumentStatus.uploaded,
        created_at=now,
        updated_at=now,
    )
    db_session.add(doc)
    db_session.commit()

    # Caller has membership only in org1, so should not access org2 doc.
    r = client.get(f"/v1/organizations/{org2}/documents/{doc.id}")
    assert r.status_code in (403, 404)


def test_complete_upload_enqueues_job(monkeypatch, client, db_session: Session, seeded_orgs) -> None:
    now = datetime.now(UTC)
    user_id = seeded_orgs["user"]
    org1 = seeded_orgs["org1"]

    doc = Document(
        id=uuid.uuid4(),
        organization_id=org1,
        uploaded_by_id=user_id,
        storage_key="k1",
        type="egrn",
        original_filename="a.pdf",
        mime_type="application/pdf",
        size_bytes=10,
        pages_count=0,
        status=DocumentStatus.pending_upload,
        created_at=now,
        updated_at=now,
    )
    db_session.add(doc)
    db_session.commit()

    called = {"enqueued": False, "doc_id": None}

    from buildlaw_api.services import queue_service, storage_service

    monkeypatch.setattr(storage_service, "head_object_exists", lambda *_args, **_kwargs: True)

    def _enqueue(doc_id):
        called["enqueued"] = True
        called["doc_id"] = str(doc_id)

    monkeypatch.setattr(queue_service, "enqueue_process_document", _enqueue)

    r = client.post(f"/v1/organizations/{org1}/documents/{doc.id}/complete-upload")
    assert r.status_code == 200
    data = r.json()
    assert data["queued"] is True
    assert called["enqueued"] is True
    assert called["doc_id"] == str(doc.id)

