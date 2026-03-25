import uuid as uuid_mod
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp_server import db
from gbp_server.models import Dataset
from gbp_server.schemas import DatasetCreate, DatasetRead

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


@router.post("/", status_code=201)
def create_dataset(
    data: DatasetCreate, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    dataset_id = uuid_mod.uuid4()
    dataset = Dataset(id=dataset_id, **data.model_dump())
    dataset.stac_version = "1.1.0"
    if not dataset.stac_id:
        dataset.stac_id = str(dataset_id)
    if not dataset.datetime:
        dataset.datetime = datetime.now(timezone.utc)
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    return {"id": dataset.id}


@router.get("/")
def list_datasets(session: Session = Depends(db.get_session)) -> list[DatasetRead]:
    return [
        DatasetRead.model_validate(d)
        for d in session.execute(select(Dataset)).scalars().all()
    ]


@router.get("/{id}")
def get_dataset(id: UUID, session: Session = Depends(db.get_session)) -> DatasetRead:
    dataset = session.get(Dataset, id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return DatasetRead.model_validate(dataset)


@router.put("/{id}")
def update_dataset(
    id: UUID, data: DatasetCreate, session: Session = Depends(db.get_session)
) -> DatasetRead:
    existing = session.get(Dataset, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Dataset not found")
    for key, value in data.model_dump().items():
        setattr(existing, key, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return DatasetRead.model_validate(existing)


@router.delete("/{id}", status_code=204)
def delete_dataset(id: UUID, session: Session = Depends(db.get_session)) -> None:
    dataset = session.get(Dataset, id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    session.delete(dataset)
    session.commit()
