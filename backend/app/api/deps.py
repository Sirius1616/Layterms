import jwt
from jwt.exceptions import InvalidTokenError
from collections.abc import Generator
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.models import User, TokenPayload
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, create_engine
from app.core.config import settings
from app.crud import get_user_by_email


engine = create_engine(str(settings.DATABASE_URI))

reusable_outh2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token")

TokenDep = Annotated[str, Depends(reusable_outh2)]

def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, 
                             algorithms=settings.ALGORITHM)
        token_data = TokenPayload(**payload)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Credentials cannot be verified"
        )
    user_email = token_data.sub
    user = get_user_by_email(session, user_email)
    if not user:
        raise HTTPException(
            status_code=404, detail="user not found"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="user is inactive")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_admin_user(session: SessionDep, current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied"
        )
    return current_user
