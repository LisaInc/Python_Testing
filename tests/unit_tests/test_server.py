import re
import pytest
from tests.conftest import client
import server


def test_index(client):
    app, templates = client
    response = app.get("/")
    assert response.status_code == 200


def test_showSummary_valid_email(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    template, context = templates[0]
    assert rv.status_code == 200
    assert context["club"] == clubs[0]
    assert context["competitions"] == competitions


def test_showSummary_invalid_email(client):
    app, templates = client
    rv = app.post(
        "/showSummary", data=dict(email="wrong@gmail.com"), follow_redirects=True
    )
    data = rv.data.decode()

    assert rv.status_code == 200
    assert "Email not found, try again" in data


def test_purchasePlaces_valid_club_points(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    club_points_before = int(clubs[0]["points"])
    competitions_places_before = int(competitions[0]["numberOfPlaces"])
    rv = app.post(
        "/purchasePlaces",
        data=dict(
            club=clubs[0]["name"], competition=competitions[0]["name"], places=10
        ),
        follow_redirects=True,
    )
    template, context = templates[0]
    data = rv.data.decode()
    assert rv.status_code == 200
    # assert context["club"]["points"] == club_points_before - 10
    assert (
        context["competitions"][0]["numberOfPlaces"] == competitions_places_before - 10
    )
    assert "Great-booking complete!" in data


def test_purchasePlaces_invalid_points(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    club_points_before = int(clubs[0]["points"])
    competitions_places_before = competitions[1]["numberOfPlaces"]
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[1]["name"], competition=competitions[0]["name"], places=8),
        follow_redirects=True,
    )
    template, context = templates[0]
    data = rv.data.decode()
    assert rv.status_code == 2200
    assert "Your club don&#39;t have enought points" in data
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert context["club"]["points"] == club_points_before


def test_purchasePlaces_invalid_points(client):
    app, templates = client
    clubs = server.loadClubs()
    club_points_before = clubs[0]["points"]
    competitions = server.loadCompetitions()
    competitions_places_before = competitions[0]["numberOfPlaces"]
    rv = app.post(
        "/purchasePlaces",
        data=dict(
            club=clubs[0]["name"], competition=competitions[0]["name"], places=20
        ),
        follow_redirects=True,
    )
    data = rv.data.decode()
    template, context = templates[0]
    assert rv.status_code == 200
    assert "You can&#39;t book more than 12 places per competition" in data
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert context["club"]["points"] == club_points_before


def test_purchasePlaces_invalid_competition_points(client):
    app, templates = client
    clubs = server.loadClubs()
    club_points_before = clubs[0]["points"]
    competitions = server.loadCompetitions()
    competitions_places_before = competitions[1]["numberOfPlaces"]
    rv = app.post(
        "/purchasePlaces",
        data=dict(
            club=clubs[0]["name"], competition=competitions[1]["name"], places=12
        ),
        follow_redirects=True,
    )
    data = rv.data.decode()
    template, context = templates[0]
    assert rv.status_code == 200
    assert "There is not enought place in this competition" in data
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert context["club"]["points"] == club_points_before


def test_past_competition_display(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    data = rv.data.decode()
    # print(data)
    assert rv.status_code == 200
    assert f'<a href="/book/Comp1/Club1">Book Places</a>' in data
    assert f'<a href="/book/Comp2/Club1">Book Places</a>' in data
    assert f'<a href="/book/Comp3/Club1">Book Places</a>' not in data
