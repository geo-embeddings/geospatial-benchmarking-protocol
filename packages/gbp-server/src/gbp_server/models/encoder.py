import uuid

from sqlalchemy.orm import Mapped, mapped_column

from gbp_server.models.base import Base


class Encoder(Base):
    """A benchmarking encoder."""

    __tablename__ = "encoder"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
