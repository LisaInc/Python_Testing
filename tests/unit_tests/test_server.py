from tests.conftest import client
import server


def test_index(client):
    app, templates = client
    response = app.get("/")
    assert response.status_code == 200


def test_logout(client):
    app, templates = client
    response = app.get("logout", follow_redirects=True)
    template, context = templates[0]
    assert response.status_code == 200
    assert template.name == "index.html"


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
    assert context["clubs"] == clubs


def test_showSummary_invalid_email(client):
    app, templates = client
    rv = app.post(
        "/showSummary", data=dict(email="wrong@gmail.com"), follow_redirects=True
    )
    data = rv.data.decode()

    assert rv.status_code == 200
    assert "Email not found, try again" in data


def test_book_valid_url(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    url = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    rv = app.get(url, follow_redirects=True)
    assert rv.status_code == 200


def test_book_invalid_url(client):
    app, templates = client
    url = f"book/test/test"
    rv = app.get(url, follow_redirects=True)
    assert rv.status_code == 404


def test_purchasePlaces_valid(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    club_points_before = int(clubs[0]["points"])
    competitions_places_before = int(competitions[0]["numberOfPlaces"])
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[0]["name"], competition=competitions[0]["name"], places=3),
        follow_redirects=True,
    )
    template, context = templates[0]
    data = rv.data.decode()
    assert rv.status_code == 200
    assert context["club"]["points"] == club_points_before - 3 * 3
    assert (
        context["competitions"][0]["numberOfPlaces"] == competitions_places_before - 3
    )
    assert "Great-booking complete!" in data


def test_purchasePlaces_invalid_club_points(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    club_points_before = clubs[1]["points"]
    competitions_places_before = competitions[0]["numberOfPlaces"]
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[1]["name"], competition=competitions[0]["name"], places=8),
        follow_redirects=True,
    )
    template, context = templates[0]
    data = rv.data.decode()
    assert rv.status_code == 200
    assert context["message"] == "Your club don't have enought points"
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert context["club"]["points"] == club_points_before


def test_purchasePlaces_invalid_places(client):
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
    assert context["message"] == "You can't book more than 12 places per competition"
    assert context["competition"]["numberOfPlaces"] == competitions_places_before
    assert context["club"]["points"] == club_points_before


def test_purchasePlaces_invalid_competition_places(client):
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
    assert context["message"] == "There is not enought place in this competition"
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
    assert rv.status_code == 200
    assert f'<a href="/book/Comp1/Club1">Book Places</a>' in data
    assert f'<a href="/book/Comp2/Club1">Book Places</a>' in data
    assert f'<a href="/book/Comp3/Club1">Book Places</a>' not in data


def test_loadClub():
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    assert server.loadClubs() == clubs


def test_loadCompetition():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
        {"name": "Test", "date": "2022-10-22 13:30:00", "numberOfPlaces": "8"},
    ]
    assert server.loadCompetitions() == competitions
