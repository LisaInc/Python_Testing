"""  """

import pytest
import server

# from utilities import clear_all


@pytest.fixture
def mock_loadClubs(monkeypatch):
    def mock_clubs():
        return [
            {"name": "Club1", "email": "valid@test.co", "points": "15"},
            {"name": "Club2", "email": "admin@test.com", "points": "4"},
        ]

    monkeypatch.setattr(server, "loadClubs", mock_clubs)


@pytest.fixture
def mock_loadCompetitions(monkeypatch):
    def mock_competitions():
        return [
            {
                "name": "Comp1",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Comp2",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "10",
            },
        ]

    monkeypatch.setattr(server, "loadCompetitions", mock_competitions)


@pytest.fixture
def client(mock_loadCompetitions, mock_loadClubs):
    app = server.create_app()
    # clear_all()
    with app.test_client() as client:
        yield client
