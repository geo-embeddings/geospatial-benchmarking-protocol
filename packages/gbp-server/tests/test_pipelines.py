def test_create_and_get(client):
    encoder_id = client.post("/api/encoders/", json={}).json()["id"]
    decoder_id = client.post("/api/decoders/", json={}).json()["id"]

    response = client.post(
        "/api/pipelines/",
        json={"encoder_id": encoder_id, "decoder_id": decoder_id},
    )
    assert response.status_code == 201
    pipeline_id = response.json()["id"]

    response = client.get(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 200
    assert response.json()["encoder_id"] == encoder_id
    assert response.json()["decoder_id"] == decoder_id


def test_create_missing_encoder(client):
    decoder_id = client.post("/api/decoders/", json={}).json()["id"]

    response = client.post(
        "/api/pipelines/",
        json={
            "encoder_id": "00000000-0000-0000-0000-000000000000",
            "decoder_id": decoder_id,
        },
    )
    assert response.status_code == 422


def test_create_missing_decoder(client):
    encoder_id = client.post("/api/encoders/", json={}).json()["id"]

    response = client.post(
        "/api/pipelines/",
        json={
            "encoder_id": encoder_id,
            "decoder_id": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert response.status_code == 422


def test_delete(client):
    encoder_id = client.post("/api/encoders/", json={}).json()["id"]
    decoder_id = client.post("/api/decoders/", json={}).json()["id"]
    pipeline_id = client.post(
        "/api/pipelines/",
        json={"encoder_id": encoder_id, "decoder_id": decoder_id},
    ).json()["id"]

    response = client.delete(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 204

    response = client.get(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 404
