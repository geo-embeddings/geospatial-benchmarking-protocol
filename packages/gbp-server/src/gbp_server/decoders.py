from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp_server import db
from gbp_server.models import Decoder
from gbp_server.schemas import DecoderRead

router = APIRouter(prefix="/api/decoders", tags=["decoders"])


@router.post("/", status_code=201)
def create_decoder(session: Session = Depends(db.get_session)) -> dict[str, UUID]:
    decoder = Decoder()
    session.add(decoder)
    session.commit()
    session.refresh(decoder)
    return {"id": decoder.id}


@router.get("/")
def list_decoders(session: Session = Depends(db.get_session)) -> list[DecoderRead]:
    return [
        DecoderRead.model_validate(d)
        for d in session.execute(select(Decoder)).scalars().all()
    ]


@router.get("/{id}")
def get_decoder(id: UUID, session: Session = Depends(db.get_session)) -> DecoderRead:
    decoder = session.get(Decoder, id)
    if not decoder:
        raise HTTPException(status_code=404, detail="Decoder not found")
    return DecoderRead.model_validate(decoder)


@router.delete("/{id}", status_code=204)
def delete_decoder(id: UUID, session: Session = Depends(db.get_session)) -> None:
    decoder = session.get(Decoder, id)
    if not decoder:
        raise HTTPException(status_code=404, detail="Decoder not found")
    session.delete(decoder)
    session.commit()
