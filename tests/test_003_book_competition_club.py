from server import app, loadCompetitions
import pytest


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestBookCompetitionClub:
    """
    Booking page test - booking.html
    :tests:
    test_book_page_display
        :returns:
            status code OK test
            content test :
                competitions details (matches with competitions.json)
                places available (matches with clubs.json)
    """
    def test_book_page_display(self, client):
        competitions = loadCompetitions()
        response = client.get(
            "/book/" + competitions[0]["name"] + "/Simply Lift")
        data = response.data.decode()
        assert response.status_code == 200

        assert competitions[0]["name"] in data
        assert "Places available: " +\
            competitions[0]["numberOfPlaces"] in data
