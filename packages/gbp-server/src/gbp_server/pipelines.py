from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp_server import db
from gbp_server.models import Decoder, Encoder, Pipeline
from gbp_server.schemas import PipelineCreate, PipelineRead

router = APIRouter(prefix="/api/pipelines", tags=["pipelines"])


@router.post("/", status_code=201)
def create_pipeline(
    data: PipelineCreate, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    if not session.get(Encoder, data.encoder_id):
        raise HTTPException(status_code=422, detail="Encoder not found")
    if not session.get(Decoder, data.decoder_id):
        raise HTTPException(status_code=422, detail="Decoder not found")
    pipeline = Pipeline(**data.model_dump())
    session.add(pipeline)
    session.commit()
    session.refresh(pipeline)
    return {"id": pipeline.id}


@router.get("/")
def list_pipelines(session: Session = Depends(db.get_session)) -> list[PipelineRead]:
    return [
        PipelineRead.model_validate(p)
        for p in session.execute(select(Pipeline)).scalars().all()
    ]


@router.get("/{id}")
def get_pipeline(id: UUID, session: Session = Depends(db.get_session)) -> PipelineRead:
    pipeline = session.get(Pipeline, id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return PipelineRead.model_validate(pipeline)


@router.put("/{id}")
def update_pipeline(
    id: UUID, data: PipelineCreate, session: Session = Depends(db.get_session)
) -> PipelineRead:
    existing = session.get(Pipeline, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    if not session.get(Encoder, data.encoder_id):
        raise HTTPException(status_code=422, detail="Encoder not found")
    if not session.get(Decoder, data.decoder_id):
        raise HTTPException(status_code=422, detail="Decoder not found")
    for key, value in data.model_dump().items():
        setattr(existing, key, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return PipelineRead.model_validate(existing)


@router.delete("/{id}", status_code=204)
def delete_pipeline(id: UUID, session: Session = Depends(db.get_session)) -> None:
    pipeline = session.get(Pipeline, id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    session.delete(pipeline)
    session.commit()
