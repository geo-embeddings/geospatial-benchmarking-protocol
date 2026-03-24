from uuid import UUID

from pydantic import BaseModel


class Result(BaseModel):
    """A benchmarking result."""

    dataset_id: UUID
