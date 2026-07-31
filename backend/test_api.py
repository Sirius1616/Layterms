from fastapi import FastAPI
from sqlmodel import Session

from app.api.main import api_router
from app.core.db import engine, create_super_user

with Session(engine) as session:
    create_super_user(session)

app = FastAPI()
app.include_router(api_router)