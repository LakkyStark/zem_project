from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from buildlaw_api.core.security import create_access_token
from buildlaw_api.db.session import get_db
from buildlaw_api.schemas.auth import RegisterRequest, TokenResponse
from buildlaw_api.schemas.user import UserResponse
from buildlaw_api.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, db: Annotated[Session, Depends(get_db)]) -> UserResponse:
    user = auth_service.register_account(db, data)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """Поле `username` в форме — это email пользователя (совместимость с OAuth2 Password)."""
    user = auth_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)
