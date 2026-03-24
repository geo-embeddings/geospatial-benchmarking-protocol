from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp_server.models import Dataset
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


@router.post("/", status_code=201)
def create_dataset(
    dataset: Dataset, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    dataset = Dataset.model_validate(dataset)
    dataset.stac_version = "1.1.0"
    if not dataset.stac_id:
        dataset.stac_id = str(dataset.id)
    if not dataset.datetime:
        dataset.datetime = datetime.now(timezone.utc)
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    return {"id": dataset.id}


@router.get("/")
def list_datasets(session: Session = Depends(db.get_session)) -> list[Dataset]:
    return list(session.exec(select(Dataset)).all())


@router.get("/{id}")
def get_dataset(id: UUID, session: Session = Depends(db.get_session)) -> Dataset:
    dataset = session.get(Dataset, id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.put("/{id}")
def update_dataset(
    id: UUID, dataset: Dataset, session: Session = Depends(db.get_session)
) -> Dataset:
    existing = session.get(Dataset, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Dataset not found")
    dataset = Dataset.model_validate(dataset)
    existing.sqlmodel_update(dataset.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_dataset(id: UUID, session: Session = Depends(db.get_session)) -> None:
    dataset = session.get(Dataset, id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    session.delete(dataset)
    session.commit()
