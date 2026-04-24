from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from buildlaw_api.core.security import get_password_hash, verify_password
from buildlaw_api.models.enums import MembershipRole
from buildlaw_api.models.membership import Membership
from buildlaw_api.models.organization import Organization
from buildlaw_api.models.user import User
from buildlaw_api.schemas.auth import RegisterRequest


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def register_account(db: Session, data: RegisterRequest) -> User:
    if get_user_by_email(db, str(data.email)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )

    user = User(
        email=str(data.email),
        password_hash=get_password_hash(data.password),
        full_name=data.full_name,
    )
    org = Organization(name=data.organization_name)
    db.add_all([user, org])
    db.flush()

    membership = Membership(
        organization_id=org.id,
        user_id=user.id,
        role=MembershipRole.owner,
    )
    db.add(membership)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь отключён")
    return user
