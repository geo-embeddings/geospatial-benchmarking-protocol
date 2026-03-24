PRETRAINED_MODEL_DATA = {
    "pretraining_bands": "RGB",
    "preferred_satellite_source": "Sentinel-2",
    "input_shape": "3x224x224",
    "output_shape": "768",
    "pretrained_weight_source": "https://example.com/weights.pt",
    "pretraining_data_provenance": "ImageNet",
}


def _create_dependencies(client, dataset_name="test", tags=None):
    dataset_id = client.post(
        "/api/datasets/", json={"name": dataset_name, "tags": tags or []}
    ).json()["id"]
    model_id = client.post(
        "/api/pretrained-models/", json=PRETRAINED_MODEL_DATA
    ).json()["id"]
    runner_id = client.post("/api/runners/", json={}).json()["id"]
    return dataset_id, model_id, runner_id


def test_create_and_get(client):
    dataset_id, model_id, runner_id = _create_dependencies(client)

    response = client.post(
        "/api/results/",
        json={
            "dataset_id": dataset_id,
            "pretrained_model_id": model_id,
            "runner_id": runner_id,
        },
    )
    assert response.status_code == 201
    result_id = response.json()["id"]

    response = client.get(f"/api/results/{result_id}")
    assert response.status_code == 200
    assert response.json()["dataset_id"] == dataset_id
    assert response.json()["pretrained_model_id"] == model_id
    assert response.json()["runner_id"] == runner_id


def test_create_missing_dataset(client):
    _, model_id, runner_id = _create_dependencies(client)

    response = client.post(
        "/api/results/",
        json={
            "dataset_id": "00000000-0000-0000-0000-000000000000",
            "pretrained_model_id": model_id,
            "runner_id": runner_id,
        },
    )
    assert response.status_code == 422


def test_create_missing_pretrained_model(client):
    dataset_id, _, runner_id = _create_dependencies(client)

    response = client.post(
        "/api/results/",
        json={
            "dataset_id": dataset_id,
            "pretrained_model_id": "00000000-0000-0000-0000-000000000000",
            "runner_id": runner_id,
        },
    )
    assert response.status_code == 422


def test_create_missing_runner(client):
    dataset_id, model_id, _ = _create_dependencies(client)

    response = client.post(
        "/api/results/",
        json={
            "dataset_id": dataset_id,
            "pretrained_model_id": model_id,
            "runner_id": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert response.status_code == 422


def test_list_and_filter_by_tag(client):
    d1, model_id, runner_id = _create_dependencies(
        client, dataset_name="tagged", tags=["satellite"]
    )
    d2, _, _ = _create_dependencies(client, dataset_name="untagged", tags=[])

    client.post(
        "/api/results/",
        json={
            "dataset_id": d1,
            "pretrained_model_id": model_id,
            "runner_id": runner_id,
        },
    )
    client.post(
        "/api/results/",
        json={
            "dataset_id": d2,
            "pretrained_model_id": model_id,
            "runner_id": runner_id,
        },
    )

    response = client.get("/api/results/")
    assert len(response.json()) == 2

    response = client.get("/api/results/?tag=satellite")
    assert len(response.json()) == 1
    assert response.json()[0]["dataset_id"] == d1


def test_delete(client):
    dataset_id, model_id, runner_id = _create_dependencies(client)
    result_id = client.post(
        "/api/results/",
        json={
            "dataset_id": dataset_id,
            "pretrained_model_id": model_id,
            "runner_id": runner_id,
        },
    ).json()["id"]

    response = client.delete(f"/api/results/{result_id}")
    assert response.status_code == 204

    response = client.get(f"/api/results/{result_id}")
    assert response.status_code == 404
