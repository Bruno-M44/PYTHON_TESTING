from server import app, loadCompetitions
import json
import pytest


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
                reset of competitions.json
    test_with_places_number_beyond_the_available_one
        :returns:
            status code OK test
            content test :
                alert message test
    test_with_no_place
        :returns:
            status code OK test
            content test :
                alert message test
    test_with_place_no_numeric
        :returns:
            status code OK test
            content test :
                alert message test
    """
    def test_with_places_number_below_the_available_one(self, client):
        competitions = loadCompetitions()
        number_of_initial_places = competitions[0]["numberOfPlaces"]
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

        assert competitions[0]["name"] in data

        assert "Number of Places: " +\
            str(number_of_remaining_places) in data

        assert "Great-booking complete!" in data

        competitions = loadCompetitions()
        assert str(number_of_remaining_places) ==\
            competitions[0]["numberOfPlaces"]

        competitions[0]["numberOfPlaces"] = str(number_of_initial_places)
        with open('competitions.json', "w") as comps:
            json.dump({"competitions": competitions}, comps)

    def test_with_places_number_beyond_the_available_one(self, client):
        places = 68
        response = client.post(
            "/purchasePlaces", data={"places": places,
                                     "club": "Simply Lift",
                                     "competition": "Spring Festival"
                                     })
        assert response.status_code == 200

        data = response.data.decode()

        assert "Please fill a number of places less than or equal to number" +\
            " of places available" in data

    def test_with_no_place(self, client):
        places = ""
        response = client.post(
            "/purchasePlaces", data={"places": places,
                                     "club": "Simply Lift",
                                     "competition": "Spring Festival"
                                     })
        assert response.status_code == 200

        data = response.data.decode()

        assert "Please enter a number" in data

    def test_with_place_no_numeric(self, client):
        places = "rgt"
        response = client.post(
            "/purchasePlaces", data={"places": places,
                                     "club": "Simply Lift",
                                     "competition": "Spring Festival"
                                     })
        assert response.status_code == 200

        data = response.data.decode()

        assert "Please enter a number" in data
