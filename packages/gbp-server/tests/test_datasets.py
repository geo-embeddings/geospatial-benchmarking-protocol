def test_create_and_get(client):
    response = client.post("/api/datasets/", json={"name": "test", "tags": ["a", "b"]})
    assert response.status_code == 201
    dataset_id = response.json()["id"]

    response = client.get(f"/api/datasets/{dataset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test"
    assert data["tags"] == ["a", "b"]


def test_list(client):
    client.post("/api/datasets/", json={"name": "one", "tags": []})
    client.post("/api/datasets/", json={"name": "two", "tags": []})

    response = client.get("/api/datasets/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update(client):
    response = client.post("/api/datasets/", json={"name": "old", "tags": []})
    dataset_id = response.json()["id"]

    response = client.put(
        f"/api/datasets/{dataset_id}", json={"name": "new", "tags": ["x"]}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "new"
    assert response.json()["tags"] == ["x"]


def test_delete(client):
    response = client.post("/api/datasets/", json={"name": "gone", "tags": []})
    dataset_id = response.json()["id"]

    response = client.delete(f"/api/datasets/{dataset_id}")
    assert response.status_code == 204

    response = client.get(f"/api/datasets/{dataset_id}")
    assert response.status_code == 404


def test_get_not_found(client):
    response = client.get("/api/datasets/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
