from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_get_all_state_returns_all_five_stages():
    response = client.get("/state")
    assert response.status_code == 200

    body = response.json()
    assert set(body.keys()) == {
        "raw_water",
        "dosing",
        "filtration",
        "disinfection",
        "distribution",
    }


def test_get_single_stage_state():
    response = client.get("/state/dosing")
    assert response.status_code == 200
    assert "ph_value" in response.json()


def test_get_unknown_stage_returns_404():
    response = client.get("/state/not-a-stage")
    assert response.status_code == 404


def test_actuate_dosing_pump_speed():
    response = client.post("/actuate/dosing", json={"values": {"pump_speed": 55}})
    assert response.status_code == 200
    assert response.json()["pump_speed"] == 55.0

    follow_up = client.get("/state/dosing")
    assert follow_up.json()["pump_speed"] == 55.0


def test_actuate_unknown_key_returns_400():
    response = client.post("/actuate/dosing", json={"values": {"not_a_field": 1}})
    assert response.status_code == 400


def test_actuate_non_actuable_stage_returns_404():
    response = client.post("/actuate/filtration", json={"values": {"turbidity_in": 5}})
    assert response.status_code == 404
