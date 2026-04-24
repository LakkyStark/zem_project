from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from buildlaw_api.models.membership import Membership
from buildlaw_api.models.organization import Organization


def list_organizations_for_user(db: Session, user_id: UUID) -> list[tuple[Organization, Membership]]:
    stmt = (
        select(Organization, Membership)
        .join(Membership, Membership.organization_id == Organization.id)
        .where(Membership.user_id == user_id)
        .order_by(Organization.name)
    )
    rows = db.execute(stmt).all()
    return [(org, m) for org, m in rows]
