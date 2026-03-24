from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class PretrainedModel(SQLModel, table=True):
    """A pretrained model specification."""

    __tablename__ = "pretrained_model"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    pretraining_bands: str
    preferred_satellite_source: str
    input_shape: str
    output_shape: str
    pretrained_weight_source: str
    pretraining_data_provenance: str
