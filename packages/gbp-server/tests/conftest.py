import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from gbp.server import app, db
from gbp.server.models import Base


@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:17", driver="psycopg") as pg:
        yield pg


@pytest.fixture(scope="session")
def engine(postgres):
    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def client(engine):
    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[db.get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()

    with Session(engine) as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
