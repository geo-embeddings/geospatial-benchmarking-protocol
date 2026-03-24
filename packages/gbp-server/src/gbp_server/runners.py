from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from gbp_server.models import Runner
from sqlmodel import Session, select

from gbp_server import db

router = APIRouter(prefix="/api/runners", tags=["runners"])


@router.post("/", status_code=201)
def create_runner(
    runner: Runner, session: Session = Depends(db.get_session)
) -> dict[str, UUID]:
    session.add(runner)
    session.commit()
    session.refresh(runner)
    return {"id": runner.id}


@router.get("/")
def list_runners(session: Session = Depends(db.get_session)) -> list[Runner]:
    return list(session.exec(select(Runner)).all())


@router.get("/{id}")
def get_runner(id: UUID, session: Session = Depends(db.get_session)) -> Runner:
    runner = session.get(Runner, id)
    if not runner:
        raise HTTPException(status_code=404, detail="Runner not found")
    return runner


@router.put("/{id}")
def update_runner(
    id: UUID, runner: Runner, session: Session = Depends(db.get_session)
) -> Runner:
    existing = session.get(Runner, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Runner not found")
    existing.sqlmodel_update(runner.model_dump(exclude={"id"}))
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{id}", status_code=204)
def delete_runner(id: UUID, session: Session = Depends(db.get_session)) -> None:
    runner = session.get(Runner, id)
    if not runner:
        raise HTTPException(status_code=404, detail="Runner not found")
    session.delete(runner)
    session.commit()
