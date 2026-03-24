from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

from gbp_server.models import Dataset
from gbp_server import db

router = APIRouter(prefix="/stac", tags=["stac"])

STAC_VERSION = "1.1.0"
CONFORMANCE_CLASSES = [
    "https://api.stacspec.org/v1.0.0/core",
    "https://api.stacspec.org/v1.0.0/ogcapi-features",
    "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
    "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
]


def _get_all_tags(session: Session) -> list[str]:
    datasets = session.exec(select(Dataset)).all()
    return sorted({tag for d in datasets for tag in (d.tags or [])})


def _dataset_to_item(dataset: Dataset, request: Request) -> dict[str, Any]:
    base_url = str(request.base_url).rstrip("/")
    return {
        "type": "Feature",
        "stac_version": dataset.stac_version or STAC_VERSION,
        "id": dataset.stac_id,
        "geometry": dataset.geometry,
        "bbox": dataset.bbox,
        "properties": {
            "datetime": dataset.datetime.isoformat() + "Z"
            if dataset.datetime
            else None,
            "start_datetime": dataset.start_datetime.isoformat() + "Z"
            if dataset.start_datetime
            else None,
            "end_datetime": dataset.end_datetime.isoformat() + "Z"
            if dataset.end_datetime
            else None,
            "title": dataset.title,
            "tags": dataset.tags or [],
        },
        "links": [
            {
                "rel": "self",
                "type": "application/geo+json",
                "href": f"{base_url}/stac/collections/{tag}/items/{dataset.stac_id}",
            }
            for tag in (dataset.tags or [])
        ]
        + [
            {
                "rel": "collection",
                "type": "application/json",
                "href": f"{base_url}/stac/collections/{tag}",
            }
            for tag in (dataset.tags or [])
        ]
        + (dataset.links or []),
        "assets": dataset.assets or {},
    }


def _collection_dict(
    tag: str, datasets: list[Dataset], request: Request
) -> dict[str, Any]:
    base_url = str(request.base_url).rstrip("/")
    spatial_extent: dict[str, Any] = {"bbox": [[-180, -90, 180, 90]]}
    temporal_extent: dict[str, Any] = {"interval": [[None, None]]}

    bboxes = [d.bbox for d in datasets if d.bbox]
    if bboxes:
        spatial_extent["bbox"] = bboxes

    datetimes = [d.datetime.isoformat() + "Z" for d in datasets if d.datetime]
    if datetimes:
        temporal_extent["interval"] = [[min(datetimes), max(datetimes)]]

    return {
        "type": "Collection",
        "id": tag,
        "stac_version": STAC_VERSION,
        "description": f"Datasets tagged with '{tag}'",
        "title": tag,
        "license": "other",
        "extent": {
            "spatial": spatial_extent,
            "temporal": temporal_extent,
        },
        "links": [
            {
                "rel": "self",
                "type": "application/json",
                "href": f"{base_url}/stac/collections/{tag}",
            },
            {
                "rel": "root",
                "type": "application/json",
                "href": f"{base_url}/stac",
            },
            {
                "rel": "items",
                "type": "application/geo+json",
                "href": f"{base_url}/stac/collections/{tag}/items",
            },
        ],
    }


@router.get("/")
def landing_page(request: Request) -> dict[str, Any]:
    base_url = str(request.base_url).rstrip("/")
    return {
        "type": "Catalog",
        "id": "gbp",
        "stac_version": STAC_VERSION,
        "title": "Geospatial Benchmarking Protocol",
        "description": "STAC catalog for GBP datasets",
        "conformsTo": CONFORMANCE_CLASSES,
        "links": [
            {
                "rel": "self",
                "type": "application/json",
                "href": f"{base_url}/stac",
            },
            {
                "rel": "root",
                "type": "application/json",
                "href": f"{base_url}/stac",
            },
            {
                "rel": "conformance",
                "type": "application/json",
                "href": f"{base_url}/stac/conformance",
            },
            {
                "rel": "data",
                "type": "application/json",
                "href": f"{base_url}/stac/collections",
            },
        ],
    }


@router.get("/conformance")
def conformance() -> dict[str, list[str]]:
    return {"conformsTo": CONFORMANCE_CLASSES}


@router.get("/collections")
def list_collections(
    request: Request, session: Session = Depends(db.get_session)
) -> dict[str, Any]:
    tags = _get_all_tags(session)
    all_datasets = list(session.exec(select(Dataset)).all())
    collections = []
    for tag in tags:
        tagged = [d for d in all_datasets if tag in (d.tags or [])]
        collections.append(_collection_dict(tag, tagged, request))
    return {
        "collections": collections,
        "links": [
            {
                "rel": "self",
                "type": "application/json",
                "href": f"{str(request.base_url).rstrip('/')}/stac/collections",
            },
        ],
    }


@router.get("/collections/{collection_id}")
def get_collection(
    collection_id: str, request: Request, session: Session = Depends(db.get_session)
) -> dict[str, Any]:
    all_datasets = list(session.exec(select(Dataset)).all())
    tagged = [d for d in all_datasets if collection_id in (d.tags or [])]
    if not tagged:
        raise HTTPException(status_code=404, detail="Collection not found")
    return _collection_dict(collection_id, tagged, request)


@router.get("/collections/{collection_id}/items")
def list_collection_items(
    collection_id: str, request: Request, session: Session = Depends(db.get_session)
) -> dict[str, Any]:
    all_datasets = list(session.exec(select(Dataset)).all())
    tagged = [d for d in all_datasets if collection_id in (d.tags or [])]
    if not tagged and collection_id not in _get_all_tags(session):
        raise HTTPException(status_code=404, detail="Collection not found")
    features = [_dataset_to_item(d, request) for d in tagged]
    return {
        "type": "FeatureCollection",
        "features": features,
        "links": [
            {
                "rel": "self",
                "type": "application/geo+json",
                "href": f"{str(request.base_url).rstrip('/')}/stac/collections/{collection_id}/items",
            },
        ],
        "numberMatched": len(features),
        "numberReturned": len(features),
    }


@router.get("/collections/{collection_id}/items/{item_id}")
def get_collection_item(
    collection_id: str,
    item_id: str,
    request: Request,
    session: Session = Depends(db.get_session),
) -> dict[str, Any]:
    all_datasets = list(session.exec(select(Dataset)).all())
    match = [
        d
        for d in all_datasets
        if d.stac_id == item_id and collection_id in (d.tags or [])
    ]
    if not match:
        raise HTTPException(status_code=404, detail="Item not found")
    return _dataset_to_item(match[0], request)
