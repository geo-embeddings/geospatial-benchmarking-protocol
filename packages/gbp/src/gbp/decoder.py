from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Decoder(SQLModel, table=True):
    """A benchmarking decoder."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
