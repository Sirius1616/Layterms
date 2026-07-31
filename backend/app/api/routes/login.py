from app import crud
from typing import Annotated
from app.core.config import settings
from fastapi.responses import HTMLResponse
from app.api.deps import SessionDep, CurrentUser
from app.core.security import create_access_token, hash_password
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Depends, HTTPException, APIRouter
from app.models import UserPublic, UserUpdate, Token, AuthMessage, NewPassword
from app.utils import (create_password_reset_token, generate_password_reset_email, 
                       validate_password_reset_token, send_email)



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserPublic)
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = crud.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive")
    sub = user.email
    token = create_access_token(sub=sub, exp=settings.ACCESS_TOKEN_EXPIRE)
    return Token(access_token=token)

@router.get("/test-token")
def test_token(current_user: CurrentUser) -> UserPublic:

    return current_user


@router.post("/recover-password/{email}")
def recover_password(email: str) -> AuthMessage:
    user = crud.get_user_by_email(email=email)
    if user:
        token = create_password_reset_token(email=email)
        email_data = generate_password_reset_email(email=email, 
                                                   email_to=user.email, 
                                                   token=token)
        send_email(email_to=user.email,
                   subject=email_data.subject,
                   html_content=email_data.html_content)
        return AuthMessage(message="Reset token is sent to your mail")


@router.post("/reset-password")
def reset_password(session: SessionDep, password_update: NewPassword) -> AuthMessage:
    user_email = validate_password_reset_token(token=password_update.token)
    if not user_email:
        raise HTTPException(status_code=404, detail="Invalid token")
    user = crud.get_user_by_email(session, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid token")
    user_in = UserUpdate(password=password_update.new_password)
    crud.user_update(session=session, 
                     user_in=user_in, 
                     db_user=user)
    return AuthMessage(message="Password updated successfully")


@router.post("recover-password-html-content")
def recover_password_html(email: str, session: SessionDep) -> HTMLResponse:
    user = crud.get_user_by_email(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist on the server")
    token = create_password_reset_token(email=email)
    email_data = generate_password_reset_email(email=email, email_to=user.email, token=token)
    return HTMLResponse(content=email_data.html_content, 
                        headers={"subject": email_data.subject})


