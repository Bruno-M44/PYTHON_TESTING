from server import app, loadClubs, loadCompetitions
import pytest

listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestShowSummary:
    """
    Show summary page test - welcome.html

    :tests:

    test_access_show_summary_with_wrong_email
        :returns:
            status code Internal Server Error test : to replace by user error
            message

    test_access_show_summary_with_right_email
        :returns:
            status code OK test
            content test :
                welcome message with email
                link to Logout
                points available (matches with clubs.json)
                competitions details (matches with competitions.json)
    """
    def test_access_show_summary_with_wrong_email(self, client):
        email = "test@test.com"
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 500

    def test_access_show_summary_with_right_email(self, client):
        email = "john@simplylift.co"
        response = client.post('/showSummary', data={'email': email})
        data = response.data.decode("utf-8").replace("%20", " ")
        assert response.status_code == 200

        assert "<h2>Welcome, " + email + " </h2>" in data

        assert """<a href="/logout">Logout</a>""" in data

        assert ("Points available: " + [club["points"] for club in listOfClubs
                if club["email"] == email][0]) in data

        for competition in listOfCompetitions:
            assert competition["name"] in data
            assert "Date: " + competition["date"] in data
            assert "Number of Places: " + competition["numberOfPlaces"] in data
            assert """<a href="/book/""" + competition["name"] +\
                """/Simply Lift">Book Places</a>""" in data
