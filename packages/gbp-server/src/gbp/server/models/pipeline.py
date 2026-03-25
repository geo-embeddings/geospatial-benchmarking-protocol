import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from gbp.server.models.base import Base


class Pipeline(Base):
    """A benchmarking pipeline."""

    __tablename__ = "pipeline"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    encoder_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("encoder.id"))
    decoder_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("decoder.id"))
