import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from buildlaw_api.models.enums import DocumentStatus


class DocumentUploadSessionRequest(BaseModel):
    type: str = Field(default="other", max_length=64)
    original_filename: str = Field(max_length=512)
    mime_type: str = Field(max_length=255)
    size_bytes: int | None = Field(default=None, ge=0)


class DocumentUploadSessionResponse(BaseModel):
    document_id: uuid.UUID
    storage_key: str
    status: DocumentStatus
    upload_url: str = Field(description="Presigned URL для HTTP PUT файла")
    upload_method: str = Field(default="PUT")
    expires_in_seconds: int = Field(default=3600)


class DocumentCompleteUploadResponse(BaseModel):
    document_id: uuid.UUID
    status: DocumentStatus
    queued: bool = True


class DocumentListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    type: str
    original_filename: str
    status: DocumentStatus
    pages_count: int
    created_at: datetime


class DocumentListResponse(BaseModel):
    items: list[DocumentListItem]
    next_cursor: str | None


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    uploaded_by_id: uuid.UUID
    storage_key: str
    type: str
    original_filename: str
    mime_type: str
    size_bytes: int | None
    pages_count: int
    status: DocumentStatus
    error_message: str | None = None
    created_at: datetime


class DocumentPageResponse(BaseModel):
    page_number: int
    ocr_text: str
    confidence: float


class DocumentDetailsResponse(BaseModel):
    id: uuid.UUID
    type: str
    original_filename: str
    status: DocumentStatus
    pages_count: int
    created_at: datetime
    error_message: str | None = None
    pages: list[DocumentPageResponse] = Field(default_factory=list)
