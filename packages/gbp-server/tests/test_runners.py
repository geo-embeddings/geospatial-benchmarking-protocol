def test_crud(client):
    response = client.post("/api/runners/", json={})
    assert response.status_code == 201
    runner_id = response.json()["id"]

    response = client.get("/api/runners/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(f"/api/runners/{runner_id}")
    assert response.status_code == 200

    response = client.delete(f"/api/runners/{runner_id}")
    assert response.status_code == 204

    response = client.get(f"/api/runners/{runner_id}")
    assert response.status_code == 404
