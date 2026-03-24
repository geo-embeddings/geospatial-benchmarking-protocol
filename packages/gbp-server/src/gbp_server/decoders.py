from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp_server.models import Decoder
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/decoders", tags=["decoders"])


@router.post("/", status_code=201)
def create_decoder(
    decoder: Decoder, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    session.add(decoder)
    session.commit()
    session.refresh(decoder)
    return {"id": decoder.id}


@router.get("/")
def list_decoders(session: Session = Depends(db.get_session)) -> list[Decoder]:
    return list(session.exec(select(Decoder)).all())


@router.get("/{id}")
def get_decoder(id: UUID, session: Session = Depends(db.get_session)) -> Decoder:
    decoder = session.get(Decoder, id)
    if not decoder:
        raise HTTPException(status_code=404, detail="Decoder not found")
    return decoder


@router.put("/{id}")
def update_decoder(
    id: UUID, decoder: Decoder, session: Session = Depends(db.get_session)
) -> Decoder:
    existing = session.get(Decoder, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Decoder not found")
    existing.sqlmodel_update(decoder.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_decoder(id: UUID, session: Session = Depends(db.get_session)) -> None:
    decoder = session.get(Decoder, id)
    if not decoder:
        raise HTTPException(status_code=404, detail="Decoder not found")
    session.delete(decoder)
    session.commit()
