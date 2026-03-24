from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from gbp_server import datasets, db, pipelines, results


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    db.create_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(datasets.router)
app.include_router(pipelines.router)
app.include_router(results.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
