from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp_server.models import PretrainedModel
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/pretrained-models", tags=["pretrained-models"])


@router.post("/", status_code=201)
def create_pretrained_model(
    model: PretrainedModel, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    session.add(model)
    session.commit()
    session.refresh(model)
    return {"id": model.id}


@router.get("/")
def list_pretrained_models(
    session: Session = Depends(db.get_session),
) -> list[PretrainedModel]:
    return list(session.exec(select(PretrainedModel)).all())


@router.get("/{id}")
def get_pretrained_model(
    id: UUID, session: Session = Depends(db.get_session)
) -> PretrainedModel:
    model = session.get(PretrainedModel, id)
    if not model:
        raise HTTPException(status_code=404, detail="Pretrained model not found")
    return model


@router.put("/{id}")
def update_pretrained_model(
    id: UUID,
    model: PretrainedModel,
    session: Session = Depends(db.get_session),
) -> PretrainedModel:
    existing = session.get(PretrainedModel, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pretrained model not found")
    existing.sqlmodel_update(model.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_pretrained_model(
    id: UUID, session: Session = Depends(db.get_session)
) -> None:
    model = session.get(PretrainedModel, id)
    if not model:
        raise HTTPException(status_code=404, detail="Pretrained model not found")
    session.delete(model)
    session.commit()
