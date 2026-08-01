from sqlmodel import Session

from app.core.db import create_super_user
from app.crud import engine


def main() -> None:
    with Session(engine) as session:
        create_super_user(session)


if __name__ == "__main__":
    main()
