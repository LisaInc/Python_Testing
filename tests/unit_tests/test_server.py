import pytest
from tests.conftest import client
from server import loadClubs
import server


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_showSummary_valid_email(client):
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    print(clubs)
    rv = client.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    data = rv.data.decode()
    print(data)
    assert rv.status_code == 200
    assert clubs[0]["email"] in data
    assert f"Points available: {clubs[0]['points']}"
    for competition in competitions:
        assert competition["name"] in data


def test_showSummary_invalid_email(client):
    rv = client.post(
        "/showSummary", data=dict(email="wrong@gmail.com"), follow_redirects=True
    )
    data = rv.data.decode()

    assert rv.status_code == 200
    assert "Email not found, try again" in data


# def test_book(client):
#     # rv = client.get("/book", )
#     pass


def test_purchasePlaces_valid_points(client):
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    club_points_before = int(clubs[0]["points"])
    competitions_places_before = int(competitions[0]["numberOfPlaces"])
    rv = client.post(
        "/purchasePlaces",
        data=dict(
            club=clubs[0]["name"], competition=competitions[0]["name"], places=10
        ),
        follow_redirects=True,
    )
    data = rv.data.decode()
    assert rv.status_code == 200
    # assert clubs[0]["points"] == club_points_before - 10
    # assert competitions[0]["numberOfPlaces"] == competitions_places_before - 10
    assert "Great-booking complete!" in data


def test_purchasePlaces_invalid_points(client):
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    club_points_before = clubs[0]["points"]
    competitions_places_before = competitions[0]["numberOfPlaces"]
    rv = client.post(
        "/purchasePlaces",
        data=dict(
            club=clubs[0]["name"], competition=competitions[0]["name"], places=20
        ),
        follow_redirects=True,
    )
    data = rv.data.decode()

    assert rv.status_code == 200
    assert "Your club don&#39;t have enought points" in data
    assert clubs[0]["points"] == club_points_before
    assert competitions[0]["numberOfPlaces"] == competitions_places_before
