import jwt
from typing import Any
from pydantic import EmailStr
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.config import settings
from datetime import datetime, timedelta


hasher = PasswordHash.recommended(
    (
        Argon2Hasher(),
        BcryptHasher()
    )
)



def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> tuple[bool, str | None]:
    return hasher.verify_and_update(plain_password, hashed_password)


def create_access_token(sub: str | Any, exp: timedelta) -> str:
    expire = exp + datetime.now()
    payload = {"sub": sub, "exp": expire}
    token = jwt.encode(payload=payload, 
                       algorithm=settings.ALGORITHM, 
                       key=settings.SECRET_KEY)
    return token
