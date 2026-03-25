import uuid

from sqlalchemy.orm import Mapped, mapped_column

from gbp.server.models.base import Base


class PretrainedModel(Base):
    """A pretrained model specification."""

    __tablename__ = "pretrained_model"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    pretraining_bands: Mapped[str]
    preferred_satellite_source: Mapped[str]
    input_shape: Mapped[str]
    output_shape: Mapped[str]
    pretrained_weight_source: Mapped[str]
    pretraining_data_provenance: Mapped[str]
