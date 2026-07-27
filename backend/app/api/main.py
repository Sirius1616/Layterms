from app.api.routes import login, items, private, users
from fastapi import APIRouter


api_router = APIRouter()


api_router.include_router(login.router)
api_router.include_router(items.router)
api_router.include_router(private.router)
api_router.include_router(users.router)


