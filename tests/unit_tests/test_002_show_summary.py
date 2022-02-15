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

    test_access_show_summary_without_mail
        :returns:
            status code OK test
            content test :
                welcome message test
                input message test
                email form test
                alert message test

    test_access_show_summary_with_wrong_email
        :returns:
            status code OK test
            content test :
                welcome message test
                input message test
                email form test
                alert message test

    test_access_show_summary_with_right_email
        :returns:
            status code OK test
            content test :
                welcome message with email
                link to Logout
                points available (matches with clubs.json)
                competitions details (matches with competitions.json)
    """
    def test_access_show_summary_without_mail(self, client):
        response = client.post("/showSummary", data={'email': ""})
        assert response.status_code == 200
        data = response.data.decode()
        assert "<h1>Welcome to the GUDLFT Registration Portal!</h1>" in data
        assert "Please enter your secretary email to continue:" in data
        assert """<label for="email">Email:</label>""" in data
        assert """<input type="email" name="email" id="" required>""" in data
        assert """<button type="submit">Enter</button>""" in data
        assert """Please fill out this field""" in data

    def test_access_show_summary_with_wrong_email(self, client):
        email = "test@test.com"
        response = client.post("/showSummary", data={'email': email})
        assert response.status_code == 200
        data = response.data.decode()
        assert "<h1>Welcome to the GUDLFT Registration Portal!</h1>" in data
        assert "Please enter your secretary email to continue:" in data
        assert """<label for="email">Email:</label>""" in data
        assert """<input type="email" name="email" id="" required>""" in data
        assert """<button type="submit">Enter</button>""" in data
        assert """Please fill mail from an existing club""" in data

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
