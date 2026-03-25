import uuid

from sqlalchemy.orm import Mapped, mapped_column

from gbp_server.models.base import Base


class Runner(Base):
    """A benchmarking runner."""

    __tablename__ = "runner"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
