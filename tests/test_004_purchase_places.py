from server import app, loadClubs, loadCompetitions
import pytest

listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestPurchasePlaces:
    """
    Purches places page test - booking.html --> welcome.html
    :tests:
    test_with_places_number_below_the_available_one
        :returns:
            status code OK test
            content test :
                competition name (matches with competitions.json)
                new value for number of places
                confirmation message
                update of competitions.json
    test_access_show_summary_with_right_email
        :returns:
            status code not OK test
    """
    def test_with_places_number_below_the_available_one(self, client):
        number_of_initial_places = listOfCompetitions[0]["numberOfPlaces"]
        number_of_taken_places = 10
        number_of_remaining_places = int(number_of_initial_places) - \
            number_of_taken_places
        response = client.post(
            "/purchasePlaces", data={"places": number_of_taken_places,
                                     "club": "Simply Lift",
                                     "competition": "Spring Festival"
                                     })
        data = response.data.decode()
        assert response.status_code == 200

        assert listOfCompetitions[0]["name"] in data

        assert "Number of Places: " +\
            str(number_of_remaining_places) in data

        assert "Great-booking complete!" in data

        assert str(number_of_remaining_places) ==\
            listOfCompetitions[0]["numberOfPlaces"]

    def test_with_places_number_beyond_the_available_one(self, client):
        places = 68
        response = client.post(
            "/purchasePlaces", data={"places": places,
                                     "club": "Simply Lift",
                                     "competition": "Spring Festival"
                                     })
        assert response.status_code != 200