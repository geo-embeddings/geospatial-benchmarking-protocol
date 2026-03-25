import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from gbp.server.models.base import Base


class Result(Base):
    """A benchmarking result."""

    __tablename__ = "result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dataset.id"))
    pretrained_model_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pretrained_model.id")
    )
    runner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("runner.id"))
