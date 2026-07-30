from app.models import UserPublic, UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from fastapi import status, HTTPException, APIRouter
from app.api.deps import SessionDep
from app import crud
from app.core.security import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserPublic)
def login_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm):
    user = crud.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid usrname or password")
    sub = user.email
    token = create_access_token(sub=sub, exp=settings.ACCESS_TOKEN_EXPIRE)
    return token 