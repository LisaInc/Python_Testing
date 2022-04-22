from tests.conftest import client
from server import loadClubs, loadCompetitions

clubs = loadClubs()
competitions = loadCompetitions()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_showSummary(client):
    rv = client.post(
        "/showSummary", data=dict(email="john@simplylift.co"), follow_redirects=True
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert clubs[0]["email"] in data
    assert f"Points available: {clubs[0]['points']}"
    for competition in competitions:
        assert competition["name"] in data
    rv = client.post(
        "/showSummary", data=dict(email="wrong@gmail.com"), follow_redirects=True
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Email not found, try again" in data
