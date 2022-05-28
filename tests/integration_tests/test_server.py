import pytest
from tests.conftest import client
import server


def test_login_and_bookplace(client):
    app, templates = client
    response = app.get("/")
    assert response.status_code == 200
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    template, context = templates[1]
    assert rv.status_code == 200
    assert context["club"] == clubs[0]
    assert context["competitions"] == competitions
    assert context["clubs"] == clubs
    url = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    rv = app.get(url, follow_redirects=True)
    assert rv.status_code == 200
    club_points_before = int(clubs[0]["points"])
    competitions_places_before = int(competitions[0]["numberOfPlaces"])
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[0]["name"], competition=competitions[0]["name"], places=3),
        follow_redirects=True,
    )
    template, context = templates[3]
    data = rv.data.decode()
    assert rv.status_code == 200
    assert context["club"]["points"] == club_points_before - 3 * 3
    assert (
        context["competitions"][0]["numberOfPlaces"] == competitions_places_before - 3
    )
    assert "Great-booking complete!" in data


def test_login_logout(client):
    app, templates = client
    response = app.get("/")
    assert response.status_code == 200
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    template, context = templates[1]
    assert rv.status_code == 200
    assert context["club"] == clubs[0]
    assert context["competitions"] == competitions
    assert context["clubs"] == clubs
    response = app.get("logout", follow_redirects=True)
    template, context = templates[0]
    assert response.status_code == 200
    assert template.name == "index.html"


def test_login_fail_then_valid(client):
    app, templates = client
    rv = app.post(
        "/showSummary", data=dict(email="wrong@gmail.com"), follow_redirects=True
    )
    data = rv.data.decode()
    assert rv.status_code == 200
    assert "Email not found, try again" in data
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    template, context = templates[1]
    assert rv.status_code == 200
    assert context["club"] == clubs[0]
    assert context["competitions"] == competitions
    assert context["clubs"] == clubs


def test_bookplace_fail_then_success(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    url = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    rv = app.get(url, follow_redirects=True)

    assert rv.status_code == 200

    club_points_before = clubs[1]["points"]
    competitions_places_before = competitions[0]["numberOfPlaces"]
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[1]["name"], competition=competitions[0]["name"], places=8),
        follow_redirects=True,
    )
    template, context = templates[1]
    data = rv.data.decode()

    assert rv.status_code == 200
    assert context["message"] == "Your club don't have enought points"
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert context["club"]["points"] == club_points_before
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[1]["name"], competition=competitions[0]["name"], places=1),
        follow_redirects=True,
    )
    template, context = templates[2]
    data = rv.data.decode()

    assert rv.status_code == 200
    assert context["club"]["points"] == int(club_points_before) - 3
    assert (
        context["competitions"][0]["numberOfPlaces"]
        == int(competitions_places_before) - 1
    )
    assert "Great-booking complete!" in data


def test_bookplace_twice(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    url = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    rv = app.get(url, follow_redirects=True)

    assert rv.status_code == 200

    club_points_before = clubs[0]["points"]
    competitions_places_before = competitions[0]["numberOfPlaces"]
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[0]["name"], competition=competitions[0]["name"], places=1),
        follow_redirects=True,
    )
    template, context = templates[1]
    data = rv.data.decode()
    club_points_before = int(club_points_before) - 3
    competitions_places_before = int(competitions_places_before) - 1

    assert rv.status_code == 200
    assert context["club"]["points"] == club_points_before
    assert context["competitions"][0]["numberOfPlaces"] == competitions_places_before
    assert "Great-booking complete!" in data

    url = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    rv = app.get(url, follow_redirects=True)

    assert rv.status_code == 200

    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[0]["name"], competition=competitions[0]["name"], places=1),
        follow_redirects=True,
    )
    template, context = templates[2]
    data = rv.data.decode()
    club_points_before = int(club_points_before) - 3
    competitions_places_before = int(competitions_places_before) - 1
    print(context)
    assert rv.status_code == 200
    assert context["club"]["points"] == club_points_before
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert "Great-booking complete!" in data
