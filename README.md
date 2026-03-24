# geospatial-benchmarking-protocol

(WIP) Backend and frontend for geospatial embeddings benchmarks

## Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/)

### Backend server

```shell
uv run fastapi dev packages/gbp-server/src/gbp_server
```

This starts the server at <http://localhost:8000> with auto-reload enabled.
