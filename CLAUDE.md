# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Geospatial Benchmarking Protocol (GBP) — a monorepo with three tightly coupled packages using `gbp` namespace packaging:

- **`packages/gbp`** — Root namespace package (`gbp`)
- **`packages/gbp-server`** — FastAPI REST API server (`gbp.server`)
- **`packages/gbp-infra`** — AWS CDK infrastructure (`gbp.infra`)
- **`frontend/`** — React + TypeScript + Vite + Chakra UI frontend

The frontend generates its API types from the backend's OpenAPI schema.

## Common Commands

### Python (uses `uv`)

```sh
uv run ruff check packages/         # lint
uv run ty check                      # type check
uv run fastapi dev packages/gbp-server/src/gbp/server --host 0.0.0.0  # run backend
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
frontend → (HTTP /api/*) → gbp.server → gbp.server.models
```

- **gbp.server** has one router module per model (`datasets.py`, `pipelines.py`, `results.py`) mounted under `/api/{resource}/`. Database is PostgreSQL, schema created on startup via `db.create_db()`. Tests use `testcontainers` to spin up a real Postgres instance.
- **gbp.server.models** defines SQLAlchemy ORM table classes. Pydantic schemas for API request/response live in `gbp.server.schemas`.
- **gbp.infra** defines AWS CDK stacks for RDS PostgreSQL and Fargate deployment.
- **frontend** proxies `/api/*` to the backend via Vite config. API functions live in `src/api/`, types are auto-generated from the OpenAPI schema via `yarn generate:types`.

## Adding a New Model

1. Create `packages/gbp-server/src/gbp/server/models/{model}.py` with a SQLAlchemy ORM class
2. Add Pydantic schemas to `packages/gbp-server/src/gbp/server/schemas.py`
3. Export from `packages/gbp-server/src/gbp/server/models/__init__.py`
4. Create `packages/gbp-server/src/gbp/server/{model}s.py` with a CRUD router
5. Register the router in `packages/gbp-server/src/gbp/server/__init__.py`
6. Run `yarn generate:types` in `frontend/` to update TypeScript types
