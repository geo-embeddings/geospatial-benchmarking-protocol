import uuid

from sqlalchemy.orm import Mapped, mapped_column

from gbp.server.models.base import Base


class Decoder(Base):
    """A benchmarking decoder."""

    __tablename__ = "decoder"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
