from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from gbp import Dataset

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

_datasets: dict[UUID, Dataset] = {}


def exists(id: UUID) -> bool:
    return id in _datasets


@router.post("/", status_code=201)
async def create_dataset(dataset: Dataset) -> dict[str, UUID]:
    id = uuid4()
    _datasets[id] = dataset
    return {"id": id}


@router.get("/")
async def list_datasets() -> dict[UUID, Dataset]:
    return _datasets


@router.get("/{id}")
async def get_dataset(id: UUID) -> Dataset:
    if id not in _datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return _datasets[id]


@router.put("/{id}")
async def update_dataset(id: UUID, dataset: Dataset) -> Dataset:
    if id not in _datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    _datasets[id] = dataset
    return dataset


@router.delete("/{id}", status_code=204)
async def delete_dataset(id: UUID) -> None:
    if id not in _datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    del _datasets[id]
