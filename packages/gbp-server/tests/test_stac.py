def _create_dataset(client, name, tags):
    return client.post(
        "/api/datasets/",
        json={"title": name, "tags": tags},
    ).json()["id"]


def test_landing_page(client):
    response = client.get("/stac/")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Catalog"
    assert data["stac_version"] == "1.1.0"
    assert "conformsTo" in data
    assert any(link["rel"] == "data" for link in data["links"])


def test_conformance(client):
    response = client.get("/stac/conformance")
    assert response.status_code == 200
    assert "conformsTo" in response.json()


def test_collections_from_tags(client):
    _create_dataset(client, "Sentinel-2 RGB", ["satellite", "optical"])
    _create_dataset(client, "Sentinel-1 SAR", ["satellite", "radar"])

    response = client.get("/stac/collections")
    assert response.status_code == 200
    collections = response.json()["collections"]
    collection_ids = [c["id"] for c in collections]
    assert "satellite" in collection_ids
    assert "optical" in collection_ids
    assert "radar" in collection_ids


def test_get_collection(client):
    _create_dataset(client, "Sentinel-2 RGB", ["satellite"])

    response = client.get("/stac/collections/satellite")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Collection"
    assert data["id"] == "satellite"


def test_get_collection_not_found(client):
    response = client.get("/stac/collections/nonexistent")
    assert response.status_code == 404


def test_collection_items(client):
    _create_dataset(client, "Sentinel-2 RGB", ["satellite"])
    _create_dataset(client, "Sentinel-1 SAR", ["satellite"])
    _create_dataset(client, "DEM", ["terrain"])

    response = client.get("/stac/collections/satellite/items")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert data["numberReturned"] == 2


def test_get_item(client):
    dataset_id = _create_dataset(client, "Sentinel-2 RGB", ["satellite"])

    response = client.get(f"/stac/collections/satellite/items/{dataset_id}")
    assert response.status_code == 200
    item = response.json()
    assert item["type"] == "Feature"
    assert item["id"] == dataset_id
    assert item["properties"]["title"] == "Sentinel-2 RGB"
    assert item["properties"]["datetime"] is not None


def test_get_item_not_found(client):
    response = client.get("/stac/collections/satellite/items/nonexistent")
    assert response.status_code == 404
