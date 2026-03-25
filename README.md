# geospatial-benchmarking-protocol

<p align="center">
  <img src="frontend/public/gbp-logo.svg" alt="GBP logo" width="128" height="128">
</p>

Work-in-progress Python package, server, and simple website for building, running, and publishing geospatial foundation model benchmarks.

## Development

To run the systems locally:

```shell
docker compose up
```

This starts:

- **Frontend**: <http://localhost:5173>
- **Backend**: <http://localhost:8000>

### Without Docker

If you prefer to run the services directly, get:

- [uv](https://docs.astral.sh/uv/)
- [Node.js](https://nodejs.org/) (v20+)
- [Yarn](https://yarnpkg.com/)

```shell
uv run fastapi dev packages/gbp-server/src/gbp_server
```

```shell
cd frontend && yarn dev
```
