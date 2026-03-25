from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp_server import db
from gbp_server.models import Encoder
from gbp_server.schemas import EncoderRead

router = APIRouter(prefix="/api/encoders", tags=["encoders"])


@router.post("/", status_code=201)
def create_encoder(session: Session = Depends(db.get_session)) -> dict[str, UUID]:
    encoder = Encoder()
    session.add(encoder)
    session.commit()
    session.refresh(encoder)
    return {"id": encoder.id}


@router.get("/")
def list_encoders(session: Session = Depends(db.get_session)) -> list[EncoderRead]:
    return [
        EncoderRead.model_validate(e)
        for e in session.execute(select(Encoder)).scalars().all()
    ]


@router.get("/{id}")
def get_encoder(id: UUID, session: Session = Depends(db.get_session)) -> EncoderRead:
    encoder = session.get(Encoder, id)
    if not encoder:
        raise HTTPException(status_code=404, detail="Encoder not found")
    return EncoderRead.model_validate(encoder)


@router.delete("/{id}", status_code=204)
def delete_encoder(id: UUID, session: Session = Depends(db.get_session)) -> None:
    encoder = session.get(Encoder, id)
    if not encoder:
        raise HTTPException(status_code=404, detail="Encoder not found")
    session.delete(encoder)
    session.commit()
