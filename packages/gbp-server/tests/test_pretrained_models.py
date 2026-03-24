PRETRAINED_MODEL_DATA = {
    "pretraining_bands": "RGB",
    "preferred_satellite_source": "Sentinel-2",
    "input_shape": "3x224x224",
    "output_shape": "768",
    "pretrained_weight_source": "https://example.com/weights.pt",
    "pretraining_data_provenance": "ImageNet",
}


def test_create_and_get(client):
    response = client.post("/api/pretrained-models/", json=PRETRAINED_MODEL_DATA)
    assert response.status_code == 201
    model_id = response.json()["id"]

    response = client.get(f"/api/pretrained-models/{model_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["pretraining_bands"] == "RGB"
    assert data["preferred_satellite_source"] == "Sentinel-2"


def test_list(client):
    client.post("/api/pretrained-models/", json=PRETRAINED_MODEL_DATA)
    client.post("/api/pretrained-models/", json=PRETRAINED_MODEL_DATA)

    response = client.get("/api/pretrained-models/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update(client):
    response = client.post("/api/pretrained-models/", json=PRETRAINED_MODEL_DATA)
    model_id = response.json()["id"]

    updated = {**PRETRAINED_MODEL_DATA, "pretraining_bands": "RGBN"}
    response = client.put(f"/api/pretrained-models/{model_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["pretraining_bands"] == "RGBN"


def test_delete(client):
    response = client.post("/api/pretrained-models/", json=PRETRAINED_MODEL_DATA)
    model_id = response.json()["id"]

    response = client.delete(f"/api/pretrained-models/{model_id}")
    assert response.status_code == 204

    response = client.get(f"/api/pretrained-models/{model_id}")
    assert response.status_code == 404
