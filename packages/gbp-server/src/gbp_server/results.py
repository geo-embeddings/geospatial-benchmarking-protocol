from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp_server import db
from gbp_server.models import Dataset, PretrainedModel, Result, Runner
from gbp_server.schemas import ResultCreate, ResultRead

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("/", status_code=201)
def create_result(
    data: ResultCreate, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    if not session.get(Dataset, data.dataset_id):
        raise HTTPException(status_code=422, detail="Dataset not found")
    if not session.get(PretrainedModel, data.pretrained_model_id):
        raise HTTPException(status_code=422, detail="Pretrained model not found")
    if not session.get(Runner, data.runner_id):
        raise HTTPException(status_code=422, detail="Runner not found")
    result = Result(**data.model_dump())
    session.add(result)
    session.commit()
    session.refresh(result)
    return {"id": result.id}


@router.get("/")
def list_results(
    session: Session = Depends(db.get_session), tag: str | None = None
) -> list[ResultRead]:
    if tag:
        datasets = session.execute(select(Dataset)).scalars().all()
        dataset_ids = [d.id for d in datasets if tag in d.tags]
        results = (
            session.execute(select(Result).where(Result.dataset_id.in_(dataset_ids)))
            .scalars()
            .all()
        )
        return [ResultRead.model_validate(r) for r in results]
    return [
        ResultRead.model_validate(r)
        for r in session.execute(select(Result)).scalars().all()
    ]


@router.get("/{id}")
def get_result(id: UUID, session: Session = Depends(db.get_session)) -> ResultRead:
    result = session.get(Result, id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultRead.model_validate(result)


@router.put("/{id}")
def update_result(
    id: UUID, data: ResultCreate, session: Session = Depends(db.get_session)
) -> ResultRead:
    existing = session.get(Result, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Result not found")
    if not session.get(Dataset, data.dataset_id):
        raise HTTPException(status_code=422, detail="Dataset not found")
    if not session.get(PretrainedModel, data.pretrained_model_id):
        raise HTTPException(status_code=422, detail="Pretrained model not found")
    if not session.get(Runner, data.runner_id):
        raise HTTPException(status_code=422, detail="Runner not found")
    for key, value in data.model_dump().items():
        setattr(existing, key, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return ResultRead.model_validate(existing)


@router.delete("/{id}", status_code=204)
def delete_result(id: UUID, session: Session = Depends(db.get_session)) -> None:
    result = session.get(Result, id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    session.delete(result)
    session.commit()
