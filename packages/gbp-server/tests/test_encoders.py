def test_crud(client):
    response = client.post("/api/encoders/", json={})
    assert response.status_code == 201
    encoder_id = response.json()["id"]

    response = client.get("/api/encoders/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(f"/api/encoders/{encoder_id}")
    assert response.status_code == 200

    response = client.delete(f"/api/encoders/{encoder_id}")
    assert response.status_code == 204

    response = client.get(f"/api/encoders/{encoder_id}")
    assert response.status_code == 404
