from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp import Dataset, PretrainedModel, Result, Runner
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("/", status_code=201)
def create_result(
    result: Result, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    if not session.get(Dataset, result.dataset_id):
        raise HTTPException(status_code=422, detail="Dataset not found")
    if not session.get(PretrainedModel, result.pretrained_model_id):
        raise HTTPException(status_code=422, detail="Pretrained model not found")
    if not session.get(Runner, result.runner_id):
        raise HTTPException(status_code=422, detail="Runner not found")
    session.add(result)
    session.commit()
    session.refresh(result)
    return {"id": result.id}


@router.get("/")
def list_results(
    session: Session = Depends(db.get_session), tag: str | None = None
) -> list[Result]:
    if tag:
        dataset_ids = [
            d.id
            for d in session.exec(select(Dataset)).all()
            if tag in d.tags
        ]
        return list(
            session.exec(select(Result).where(Result.dataset_id.in_(dataset_ids))).all()
        )
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
    if not session.get(PretrainedModel, result.pretrained_model_id):
        raise HTTPException(status_code=422, detail="Pretrained model not found")
    if not session.get(Runner, result.runner_id):
        raise HTTPException(status_code=422, detail="Runner not found")
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
