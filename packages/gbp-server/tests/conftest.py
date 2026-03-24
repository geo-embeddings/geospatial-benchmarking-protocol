import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

import gbp  # noqa: F401 — registers all models on SQLModel.metadata
from gbp_server import app, db


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[db.get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()
