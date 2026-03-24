import datetime as dt
from uuid import UUID, uuid4

from sqlmodel import Column, Field, JSON, SQLModel


class Dataset(SQLModel, table=True):
    """A benchmarking dataset, modeled as a STAC Item."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    stac_version: str = Field(default="1.1.0")
    stac_id: str | None = None
    geometry: dict | None = Field(default=None, sa_column=Column(JSON))
    bbox: list[float] | None = Field(default=None, sa_column=Column(JSON))
    datetime: dt.datetime | None = None
    start_datetime: dt.datetime | None = None
    end_datetime: dt.datetime | None = None
    links: list[dict] = Field(default_factory=list, sa_column=Column(JSON))
    assets: dict = Field(default_factory=dict, sa_column=Column(JSON))
