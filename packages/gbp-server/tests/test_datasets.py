def test_create_and_get(client):
    response = client.post(
        "/api/datasets/",
        json={"title": "test", "tags": ["a", "b"]},
    )
    assert response.status_code == 201
    dataset_id = response.json()["id"]

    response = client.get(f"/api/datasets/{dataset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test"
    assert data["tags"] == ["a", "b"]
    assert data["stac_version"] == "1.1.0"
    assert data["stac_id"] == dataset_id
    assert data["datetime"] is not None


def test_create_minimal(client):
    response = client.post("/api/datasets/", json={"title": "minimal"})
    assert response.status_code == 201
    dataset_id = response.json()["id"]

    response = client.get(f"/api/datasets/{dataset_id}")
    data = response.json()
    assert data["geometry"] is None
    assert data["bbox"] is None
    assert data["links"] == []
    assert data["assets"] == {}


def test_list(client):
    client.post("/api/datasets/", json={"title": "one"})
    client.post("/api/datasets/", json={"title": "two"})

    response = client.get("/api/datasets/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update(client):
    response = client.post("/api/datasets/", json={"title": "old"})
    dataset_id = response.json()["id"]

    response = client.put(
        f"/api/datasets/{dataset_id}",
        json={"title": "new", "tags": ["x"]},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "new"
    assert response.json()["tags"] == ["x"]


def test_delete(client):
    response = client.post("/api/datasets/", json={"title": "gone"})
    dataset_id = response.json()["id"]

    response = client.delete(f"/api/datasets/{dataset_id}")
    assert response.status_code == 204

    response = client.get(f"/api/datasets/{dataset_id}")
    assert response.status_code == 404


def test_get_not_found(client):
    response = client.get("/api/datasets/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
