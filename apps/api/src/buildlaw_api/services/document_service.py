from uuid import UUID

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import and_, desc, or_, select
from sqlalchemy.orm import Session

from buildlaw_api.models.document import Document
from buildlaw_api.models.document_page import DocumentPage
from buildlaw_api.models.enums import DocumentStatus
from buildlaw_api.schemas.document import DocumentUploadSessionRequest
from buildlaw_api.services import membership_service, queue_service, storage_service


def create_upload_session(
    db: Session,
    *,
    organization_id: UUID,
    user_id: UUID,
    body: DocumentUploadSessionRequest,
) -> tuple[Document, str]:
    membership_service.require_membership(db, user_id=user_id, organization_id=organization_id)

    doc = Document(
        organization_id=organization_id,
        uploaded_by_id=user_id,
        storage_key="__pending__",
        type=body.type,
        original_filename=body.original_filename,
        mime_type=body.mime_type,
        size_bytes=body.size_bytes,
        pages_count=0,
        status=DocumentStatus.pending_upload,
    )
    db.add(doc)
    db.flush()

    key = storage_service.build_storage_key(organization_id, doc.id, body.original_filename)
    doc.storage_key = key
    db.add(doc)
    db.commit()
    db.refresh(doc)

    url = storage_service.presigned_put_url(
        storage_key=key,
        mime_type=body.mime_type,
    )
    return doc, url


def complete_upload(
    db: Session,
    *,
    organization_id: UUID,
    user_id: UUID,
    document_id: UUID,
) -> Document:
    membership_service.require_membership(db, user_id=user_id, organization_id=organization_id)

    doc = db.get(Document, document_id)
    if doc is None or doc.organization_id != organization_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")

    if doc.status != DocumentStatus.pending_upload:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Некорректный статус для завершения загрузки",
        )

    if not storage_service.head_object_exists(doc.storage_key):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Объект в хранилище не найден — загрузите файл по presigned URL",
        )

    doc.status = DocumentStatus.uploaded
    doc.error_message = None
    db.add(doc)
    db.commit()
    db.refresh(doc)

    queue_service.enqueue_process_document(doc.id)
    return doc


def list_documents(
    db: Session,
    *,
    organization_id: UUID,
    user_id: UUID,
    limit: int,
    cursor: tuple[str, str] | None,
    status: DocumentStatus | None,
    type: str | None,
) -> tuple[list[Document], str | None]:
    membership_service.require_membership(db, user_id=user_id, organization_id=organization_id)

    limit = max(1, min(100, limit))

    conditions = [Document.organization_id == organization_id]
    if status is not None:
        conditions.append(Document.status == status)
    if type is not None:
        conditions.append(Document.type == type)

    stmt = select(Document).where(and_(*conditions))

    # Cursor pagination: (created_at, id) DESC
    if cursor is not None:
        created_at_iso, id_str = cursor
        try:
            created_at_dt = datetime.fromisoformat(created_at_iso)
            cursor_id = UUID(id_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Некорректный cursor") from None
        # Compare tuple in DESC order:
        stmt = stmt.where(
            or_(
                Document.created_at < created_at_dt,
                and_(Document.created_at == created_at_dt, Document.id < cursor_id),
            )
        )

    stmt = stmt.order_by(desc(Document.created_at), desc(Document.id)).limit(limit + 1)
    docs = list(db.execute(stmt).scalars().all())

    next_cursor = None
    if len(docs) > limit:
        last = docs[limit - 1]
        next_cursor = f"{last.created_at.isoformat()}|{last.id}"
        docs = docs[:limit]

    return docs, next_cursor


def get_document_details(
    db: Session,
    *,
    organization_id: UUID,
    user_id: UUID,
    document_id: UUID,
) -> tuple[Document, list[DocumentPage]]:
    membership_service.require_membership(db, user_id=user_id, organization_id=organization_id)

    doc = db.get(Document, document_id)
    if doc is None or doc.organization_id != organization_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")

    pages = list(
        db.execute(
            select(DocumentPage)
            .where(
                DocumentPage.organization_id == organization_id,
                DocumentPage.document_id == document_id,
            )
            .order_by(DocumentPage.page_number.asc())
        )
        .scalars()
        .all()
    )
    return doc, pages
