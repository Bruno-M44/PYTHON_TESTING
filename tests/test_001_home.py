from server import app
import pytest


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestHome:
    """
    Home page Test - index.html

    :tests: test_home_page
        :returns:
            status code OK test
            content test :
                welcome message test
                input message test
                email form test
    """
    def test_home_page(self, client):
        response = client.get('/')
        data = response.data.decode()
        assert response.status_code == 200
        assert "<h1>Welcome to the GUDLFT Registration Portal!</h1>" in data
        assert "Please enter your secretary email to continue:" in data
        assert """<label for="email">Email:</label>""" in data
        assert """<input type="email" name="email" id="" required>""" in data
        assert """<button type="submit">Enter</button>""" in data
