# geospatial-benchmarking-protocol

(WIP) Backend and frontend for geospatial embeddings benchmarks

## Development

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

### Getting started

```shell
docker compose up
```

This starts both services with hot-reload enabled:

- **Backend** (FastAPI): <http://localhost:8000>
- **Frontend** (Vite + React): <http://localhost:5173>

### Without Docker

If you prefer to run the services directly:

- [uv](https://docs.astral.sh/uv/)
- [Node.js](https://nodejs.org/) (v20+)
- [Yarn](https://yarnpkg.com/)

```shell
uv run fastapi dev packages/gbp-server/src/gbp_server
```

```shell
cd frontend && yarn dev
```
