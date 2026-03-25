import datetime as dt
import uuid

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from gbp_server.models.base import Base


class Dataset(Base):
    """A benchmarking dataset, modeled as a STAC Item."""

    __tablename__ = "dataset"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    tags: Mapped[list] = mapped_column(JSON, default=list)
    stac_version: Mapped[str] = mapped_column(default="1.1.0")
    stac_id: Mapped[str | None] = mapped_column(default=None)
    geometry: Mapped[dict | None] = mapped_column(JSON, default=None)
    bbox: Mapped[list | None] = mapped_column(JSON, default=None)
    datetime: Mapped[dt.datetime | None] = mapped_column(default=None)
    start_datetime: Mapped[dt.datetime | None] = mapped_column(default=None)
    end_datetime: Mapped[dt.datetime | None] = mapped_column(default=None)
    links: Mapped[list] = mapped_column(JSON, default=list)
    assets: Mapped[dict] = mapped_column(JSON, default=dict)
