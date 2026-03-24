from uuid import UUID, uuid4

from sqlmodel import Column, Field, JSON, SQLModel


class Dataset(SQLModel, table=True):
    """A benchmarking dataset."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
