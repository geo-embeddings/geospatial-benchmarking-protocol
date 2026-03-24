from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Dataset(SQLModel, table=True):
    """A benchmarking dataset."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
