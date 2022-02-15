from server import app, loadCompetitions, loadClubs
import pytest
import json


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestLoading:
    """
    test of JSON file loading

    :tests: test_load_competitions
        :returns:
            test of file length
            test of content file

    :tests: test_load_clubs
        :returns:
            test of file length
            test of content file

    """
    def test_load_competitions(self, client):
        with open('competitions.json') as comps:
            competitions = json.load(comps)['competitions']

        assert len(competitions) == 2

        assert competitions == [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13"
            }
        ]

    def test_load_clubs(self, client):
        with open('clubs.json') as comps:
            clubs = json.load(comps)['clubs']

        assert len(clubs) == 3

        assert clubs == [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
            }
        ]
