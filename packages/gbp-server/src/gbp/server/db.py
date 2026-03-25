import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gbp.server.models import Base


def _get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    host = os.environ.get("DB_HOST")
    if host:
        port = os.environ.get("DB_PORT", "5432")
        username = os.environ.get("DB_USERNAME", "gbp")
        password = os.environ.get("DB_PASSWORD", "gbp")
        dbname = os.environ.get("DB_NAME", "gbp")
        return f"postgresql+psycopg://{username}:{password}@{host}:{port}/{dbname}"
    return "postgresql+psycopg://gbp:gbp@localhost:5432/gbp"


engine = create_engine(_get_database_url())


def create_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
