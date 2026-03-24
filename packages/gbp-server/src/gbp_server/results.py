from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from gbp import Result

router = APIRouter(prefix="/api/results", tags=["results"])

_results: dict[UUID, Result] = {}


@router.post("/", status_code=201)
async def create_result(result: Result) -> dict[str, UUID]:
    id = uuid4()
    _results[id] = result
    return {"id": id}


@router.get("/")
async def list_results() -> dict[UUID, Result]:
    return _results


@router.get("/{id}")
async def get_result(id: UUID) -> Result:
    if id not in _results:
        raise HTTPException(status_code=404, detail="Result not found")
    return _results[id]


@router.put("/{id}")
async def update_result(id: UUID, result: Result) -> Result:
    if id not in _results:
        raise HTTPException(status_code=404, detail="Result not found")
    _results[id] = result
    return result


@router.delete("/{id}", status_code=204)
async def delete_result(id: UUID) -> None:
    if id not in _results:
        raise HTTPException(status_code=404, detail="Result not found")
    del _results[id]
