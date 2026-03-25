from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from gbp.server import db
from gbp.server.models import Runner
from gbp.server.schemas import RunnerRead

router = APIRouter(prefix="/api/runners", tags=["runners"])


@router.post("/", status_code=201)
def create_runner(session: Session = Depends(db.get_session)) -> dict[str, UUID]:
    runner = Runner()
    session.add(runner)
    session.commit()
    session.refresh(runner)
    return {"id": runner.id}


@router.get("/")
def list_runners(session: Session = Depends(db.get_session)) -> list[RunnerRead]:
    return [
        RunnerRead.model_validate(r)
        for r in session.execute(select(Runner)).scalars().all()
    ]


@router.get("/{id}")
def get_runner(id: UUID, session: Session = Depends(db.get_session)) -> RunnerRead:
    runner = session.get(Runner, id)
    if not runner:
        raise HTTPException(status_code=404, detail="Runner not found")
    return RunnerRead.model_validate(runner)


@router.delete("/{id}", status_code=204)
def delete_runner(id: UUID, session: Session = Depends(db.get_session)) -> None:
    runner = session.get(Runner, id)
    if not runner:
        raise HTTPException(status_code=404, detail="Runner not found")
    session.delete(runner)
    session.commit()
