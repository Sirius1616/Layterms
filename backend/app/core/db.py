from sqlmodel import select
from app.core.config import settings
from app.api.deps import SessionDep
from app.models import User, UserCreate
from app import crud


def create_super_user(session: SessionDep) -> User:
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if not user:
        new_user = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_admin=True
        )
        crud.create_user(new_user, session)

