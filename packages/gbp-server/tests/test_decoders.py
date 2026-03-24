def test_crud(client):
    response = client.post("/api/decoders/", json={})
    assert response.status_code == 201
    decoder_id = response.json()["id"]

    response = client.get("/api/decoders/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(f"/api/decoders/{decoder_id}")
    assert response.status_code == 200

    response = client.delete(f"/api/decoders/{decoder_id}")
    assert response.status_code == 204

    response = client.get(f"/api/decoders/{decoder_id}")
    assert response.status_code == 404
