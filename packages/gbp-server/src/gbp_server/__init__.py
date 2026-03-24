from fastapi import FastAPI

from gbp_server import datasets, results

app = FastAPI()
app.include_router(datasets.router)
app.include_router(results.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
