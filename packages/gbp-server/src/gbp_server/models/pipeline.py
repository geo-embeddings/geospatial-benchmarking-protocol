from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Pipeline(SQLModel, table=True):
    """A benchmarking pipeline."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    encoder_id: UUID = Field(foreign_key="encoder.id")
    decoder_id: UUID = Field(foreign_key="decoder.id")
