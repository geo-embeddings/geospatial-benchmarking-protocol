from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Result(SQLModel, table=True):
    """A benchmarking result."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    dataset_id: UUID = Field(foreign_key="dataset.id")
    pretrained_model_id: UUID = Field(foreign_key="pretrained_model.id")
    runner_id: UUID = Field(foreign_key="runner.id")
