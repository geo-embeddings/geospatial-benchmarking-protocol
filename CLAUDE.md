# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Geospatial Benchmarking Protocol (GBP) — a monorepo with three tightly coupled packages:

- **`packages/gbp`** — Core Python library with SQLModel domain models (Dataset, Pipeline, Result)
- **`packages/gbp-server`** — FastAPI REST API server, depends on `gbp`
- **`frontend/`** — React + TypeScript + Vite + Chakra UI frontend

The frontend generates its API types from the backend's OpenAPI schema.

## Common Commands

### Python (uses `uv`)

```sh
uv run ruff check packages/         # lint
uv run ty check                      # type check
uv run fastapi dev packages/gbp-server/src/gbp_server --host 0.0.0.0  # run backend
```

### Frontend (uses `yarn`, run from `frontend/`)

```sh
yarn install --immutable   # install deps
yarn dev                   # dev server
yarn tsc -b                # type check
yarn lint                  # eslint
yarn format:check          # prettier check
yarn format                # prettier fix
yarn generate:types        # regenerate TypeScript types from backend OpenAPI schema
```

### Docker

```sh
docker compose up          # run backend + frontend
docker compose watch       # run with file-watch rebuild for frontend
```

## Architecture

```
frontend → (HTTP /api/*) → gbp-server → gbp (models)
```

- **gbp** defines SQLModel table classes. All models are re-exported from `gbp/__init__.py`.
- **gbp-server** has one router module per model (`datasets.py`, `pipelines.py`, `results.py`) mounted under `/api/{resource}/`. Database is SQLite, created on startup via `db.create_db()`.
- **frontend** proxies `/api/*` to the backend via Vite config. API functions live in `src/api/`, types are auto-generated from the OpenAPI schema via `yarn generate:types`.

## Adding a New Model

1. Create `packages/gbp/src/gbp/{model}.py` with a `SQLModel` class (`table=True`)
2. Export it from `packages/gbp/src/gbp/__init__.py`
3. Create `packages/gbp-server/src/gbp_server/{model}s.py` with a CRUD router
4. Register the router in `packages/gbp-server/src/gbp_server/__init__.py`
5. Run `yarn generate:types` in `frontend/` to update TypeScript types
