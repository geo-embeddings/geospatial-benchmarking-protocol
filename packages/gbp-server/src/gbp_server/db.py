import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///gbp.db")

engine = create_engine(DATABASE_URL)


def create_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
