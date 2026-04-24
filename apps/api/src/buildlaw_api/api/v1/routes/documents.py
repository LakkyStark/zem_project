from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from buildlaw_api.api.deps import CurrentUser
from buildlaw_api.db.session import get_db
from buildlaw_api.models.enums import DocumentStatus
from buildlaw_api.schemas.document import (
    DocumentCompleteUploadResponse,
    DocumentDetailsResponse,
    DocumentListResponse,
    DocumentUploadSessionRequest,
    DocumentUploadSessionResponse,
)
from buildlaw_api.services import document_service

router = APIRouter(prefix="/organizations/{organization_id}/documents")

@router.get("", response_model=DocumentListResponse)
def list_documents(
    organization_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
    limit: int = 20,
    cursor: str | None = None,
    status: str | None = None,
    type: str | None = None,
) -> DocumentListResponse:
    status_enum = None
    if status is not None:
        try:
            status_enum = DocumentStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Некорректный status") from None

    cursor_tuple = None
    if cursor:
        parts = cursor.split("|", 1)
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="Некорректный cursor")
        cursor_tuple = (parts[0], parts[1])

    docs, next_cursor = document_service.list_documents(
        db,
        organization_id=organization_id,
        user_id=current_user.id,
        limit=limit,
        cursor=cursor_tuple,
        status=status_enum,
        type=type,
    )
    return DocumentListResponse(
        items=[
            {
                "id": d.id,
                "type": d.type,
                "original_filename": d.original_filename,
                "status": d.status,
                "pages_count": d.pages_count,
                "created_at": d.created_at,
            }
            for d in docs
        ],
        next_cursor=next_cursor,
    )


@router.get("/{document_id}", response_model=DocumentDetailsResponse)
def get_document(
    organization_id: UUID,
    document_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
) -> DocumentDetailsResponse:
    doc, pages = document_service.get_document_details(
        db,
        organization_id=organization_id,
        user_id=current_user.id,
        document_id=document_id,
    )
    return DocumentDetailsResponse(
        id=doc.id,
        type=doc.type,
        original_filename=doc.original_filename,
        status=doc.status,
        pages_count=doc.pages_count,
        created_at=doc.created_at,
        error_message=doc.error_message,
        pages=[
            {"page_number": p.page_number, "ocr_text": p.ocr_text, "confidence": p.confidence}
            for p in pages
        ],
    )

@router.post("/upload-sessions", response_model=DocumentUploadSessionResponse, status_code=201)
def create_upload_session(
    organization_id: UUID,
    body: DocumentUploadSessionRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
) -> DocumentUploadSessionResponse:
    doc, url = document_service.create_upload_session(
        db,
        organization_id=organization_id,
        user_id=current_user.id,
        body=body,
    )
    return DocumentUploadSessionResponse(
        document_id=doc.id,
        storage_key=doc.storage_key,
        status=doc.status,
        upload_url=url,
        upload_method="PUT",
        expires_in_seconds=3600,
    )


@router.post(
    "/{document_id}/complete-upload",
    response_model=DocumentCompleteUploadResponse,
)
def complete_upload(
    organization_id: UUID,
    document_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
) -> DocumentCompleteUploadResponse:
    doc = document_service.complete_upload(
        db,
        organization_id=organization_id,
        user_id=current_user.id,
        document_id=document_id,
    )
    return DocumentCompleteUploadResponse(document_id=doc.id, status=doc.status, queued=True)
