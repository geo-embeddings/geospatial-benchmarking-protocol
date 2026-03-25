from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp.server import db
from gbp.server.models import PretrainedModel
from gbp.server.schemas import PretrainedModelCreate, PretrainedModelRead

router = APIRouter(prefix="/api/pretrained-models", tags=["pretrained-models"])


@router.post("/", status_code=201)
def create_pretrained_model(
    data: PretrainedModelCreate, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    model = PretrainedModel(**data.model_dump())
    session.add(model)
    session.commit()
    session.refresh(model)
    return {"id": model.id}


@router.get("/")
def list_pretrained_models(
    session: Session = Depends(db.get_session),
) -> list[PretrainedModelRead]:
    return [
        PretrainedModelRead.model_validate(m)
        for m in session.execute(select(PretrainedModel)).scalars().all()
    ]


@router.get("/{id}")
def get_pretrained_model(
    id: UUID, session: Session = Depends(db.get_session)
) -> PretrainedModelRead:
    model = session.get(PretrainedModel, id)
    if not model:
        raise HTTPException(status_code=404, detail="Pretrained model not found")
    return PretrainedModelRead.model_validate(model)


@router.put("/{id}")
def update_pretrained_model(
    id: UUID,
    data: PretrainedModelCreate,
    session: Session = Depends(db.get_session),
) -> PretrainedModelRead:
    existing = session.get(PretrainedModel, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pretrained model not found")
    for key, value in data.model_dump().items():
        setattr(existing, key, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return PretrainedModelRead.model_validate(existing)


@router.delete("/{id}", status_code=204)
def delete_pretrained_model(
    id: UUID, session: Session = Depends(db.get_session)
) -> None:
    model = session.get(PretrainedModel, id)
    if not model:
        raise HTTPException(status_code=404, detail="Pretrained model not found")
    session.delete(model)
    session.commit()
