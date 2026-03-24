from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Runner(SQLModel, table=True):
    """A benchmarking runner."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
