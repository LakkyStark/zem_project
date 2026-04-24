from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from buildlaw_api.models.membership import Membership


def get_membership(db: Session, *, user_id: UUID, organization_id: UUID) -> Membership | None:
    stmt = select(Membership).where(
        Membership.user_id == user_id,
        Membership.organization_id == organization_id,
    )
    return db.execute(stmt).scalar_one_or_none()


def require_membership(db: Session, *, user_id: UUID, organization_id: UUID) -> Membership:
    m = get_membership(db, user_id=user_id, organization_id=organization_id)
    if m is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к организации",
        )
    return m
