from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

from buildlaw_api.api import deps
from buildlaw_api.db.base import Base
from buildlaw_api.main import app
from buildlaw_api.models import Document, DocumentPage, Membership, Organization, User  # noqa: F401
from buildlaw_api.models.enums import MembershipRole


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def _get_db() -> Generator[Session, None, None]:
        yield db_session

    # Default test user (overridden in tests if needed)
    user = User(
        id=uuid.uuid4(),
        email="u@example.com",
        password_hash="x",
        full_name="U",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    db_session.commit()

    def _get_current_user() -> User:
        return user

    app.dependency_overrides[deps.get_db] = _get_db
    app.dependency_overrides[deps.get_current_user] = _get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture()
def seeded_orgs(db_session: Session) -> dict[str, uuid.UUID]:
    now = datetime.now(UTC)
    u1 = db_session.query(User).first()
    assert u1 is not None

    org1 = Organization(id=uuid.uuid4(), name="Org1", created_at=now, updated_at=now)
    org2 = Organization(id=uuid.uuid4(), name="Org2", created_at=now, updated_at=now)
    db_session.add_all([org1, org2])
    db_session.flush()

    m1 = Membership(
        id=uuid.uuid4(),
        organization_id=org1.id,
        user_id=u1.id,
        role=MembershipRole.owner,
        created_at=now,
    )
    db_session.add(m1)
    db_session.commit()

    return {"org1": org1.id, "org2": org2.id, "user": u1.id}

