from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gbp_server import (
    datasets,
    db,
    decoders,
    encoders,
    pipelines,
    pretrained_models,
    results,
    runners,
    stac,
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    db.create_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(datasets.router)
app.include_router(decoders.router)
app.include_router(encoders.router)
app.include_router(pipelines.router)
app.include_router(pretrained_models.router)
app.include_router(results.router)
app.include_router(runners.router)
app.include_router(stac.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
