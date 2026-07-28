import jwt
from typing import Any
from pydantic import EmailStr
from app.core.config import settings
from datetime import datetime, timedelta
from app.models import Token, TokenPayload
from jwt.exceptions import InvalidTokenError





def create_password_reset_token(email : str) -> str:
    now = datetime.now()
    expire = settings.RESET_TOKEN_EXPIRE + now
    payload = {"sub": email, 
               "exp": expire, 
               "nbf": now,
               "purpose": "password_reset"}
    token = jwt.encode(payload=payload, 
                       algorithm=settings.ALGORITHM, 
                       key=settings.SECRET_KEY)
    return token


def validate_password_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, 
                   algorithms=settings.ALGORITHM, 
                   key=settings.SECRET_KEY)
        token = payload["sub"]
        return token
    except:
        InvalidTokenError