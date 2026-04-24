from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from buildlaw_api.api.deps import CurrentUser
from buildlaw_api.db.session import get_db
from buildlaw_api.schemas.organization import OrganizationSummary
from buildlaw_api.services import organization_service

router = APIRouter()


@router.get("/", response_model=list[OrganizationSummary])
def list_my_organizations(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
) -> list[OrganizationSummary]:
    rows = organization_service.list_organizations_for_user(db, current_user.id)
    return [
        OrganizationSummary(id=org.id, name=org.name, role=m.role.value) for org, m in rows
    ]
