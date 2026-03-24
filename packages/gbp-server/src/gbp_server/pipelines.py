from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp import Pipeline
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/pipelines", tags=["pipelines"])


@router.post("/", status_code=201)
def create_pipeline(
    pipeline: Pipeline, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    session.add(pipeline)
    session.commit()
    session.refresh(pipeline)
    return {"id": pipeline.id}


@router.get("/")
def list_pipelines(session: Session = Depends(db.get_session)) -> list[Pipeline]:
    return list(session.exec(select(Pipeline)).all())


@router.get("/{id}")
def get_pipeline(id: UUID, session: Session = Depends(db.get_session)) -> Pipeline:
    pipeline = session.get(Pipeline, id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.put("/{id}")
def update_pipeline(
    id: UUID, pipeline: Pipeline, session: Session = Depends(db.get_session)
) -> Pipeline:
    existing = session.get(Pipeline, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    existing.sqlmodel_update(pipeline.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_pipeline(id: UUID, session: Session = Depends(db.get_session)) -> None:
    pipeline = session.get(Pipeline, id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    session.delete(pipeline)
    session.commit()
