from server import app, loadClubs, loadCompetitions
import pytest

listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()


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
        response = client.get(
            "/book/" + listOfCompetitions[0]["name"] + "/Simply Lift")
        data = response.data.decode()
        assert response.status_code == 200

        assert listOfCompetitions[0]["name"] in data
        assert "Places available: " +\
            listOfCompetitions[0]["numberOfPlaces"] in data
