from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp import Dataset, Pipeline, Result
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("/", status_code=201)
def create_result(
    result: Result, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    if not session.get(Dataset, result.dataset_id):
        raise HTTPException(status_code=422, detail="Dataset not found")
    if not session.get(Pipeline, result.pipeline_id):
        raise HTTPException(status_code=422, detail="Pipeline not found")
    session.add(result)
    session.commit()
    session.refresh(result)
    return {"id": result.id}


@router.get("/")
def list_results(session: Session = Depends(db.get_session)) -> list[Result]:
    return list(session.exec(select(Result)).all())


@router.get("/{id}")
def get_result(id: UUID, session: Session = Depends(db.get_session)) -> Result:
    result = session.get(Result, id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.put("/{id}")
def update_result(
    id: UUID, result: Result, session: Session = Depends(db.get_session)
) -> Result:
    existing = session.get(Result, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Result not found")
    if not session.get(Dataset, result.dataset_id):
        raise HTTPException(status_code=422, detail="Dataset not found")
    if not session.get(Pipeline, result.pipeline_id):
        raise HTTPException(status_code=422, detail="Pipeline not found")
    existing.sqlmodel_update(result.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_result(id: UUID, session: Session = Depends(db.get_session)) -> None:
    result = session.get(Result, id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    session.delete(result)
    session.commit()
