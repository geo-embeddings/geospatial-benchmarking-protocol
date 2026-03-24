from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp import Encoder
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/encoders", tags=["encoders"])


@router.post("/", status_code=201)
def create_encoder(
    encoder: Encoder, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    session.add(encoder)
    session.commit()
    session.refresh(encoder)
    return {"id": encoder.id}


@router.get("/")
def list_encoders(session: Session = Depends(db.get_session)) -> list[Encoder]:
    return list(session.exec(select(Encoder)).all())


@router.get("/{id}")
def get_encoder(id: UUID, session: Session = Depends(db.get_session)) -> Encoder:
    encoder = session.get(Encoder, id)
    if not encoder:
        raise HTTPException(status_code=404, detail="Encoder not found")
    return encoder


@router.put("/{id}")
def update_encoder(
    id: UUID, encoder: Encoder, session: Session = Depends(db.get_session)
) -> Encoder:
    existing = session.get(Encoder, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Encoder not found")
    existing.sqlmodel_update(encoder.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_encoder(id: UUID, session: Session = Depends(db.get_session)) -> None:
    encoder = session.get(Encoder, id)
    if not encoder:
        raise HTTPException(status_code=404, detail="Encoder not found")
    session.delete(encoder)
    session.commit()
