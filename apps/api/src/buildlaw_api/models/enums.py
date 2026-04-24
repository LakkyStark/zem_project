import enum


class MembershipRole(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    member = "member"


class DocumentStatus(str, enum.Enum):
    """Статусы жизненного цикла документа и фоновой обработки."""

    pending_upload = "pending_upload"
    uploaded = "uploaded"
    queued = "queued"
    ocr_done = "ocr_done"
    parsed = "parsed"
    analyzed = "analyzed"
    failed = "failed"
