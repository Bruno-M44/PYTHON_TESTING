from server import app, loadClubs
import pytest


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestHome:
    """
    Public Board page Test - public_board.html

    :tests: test_public_board
        :returns:
            status code OK test
            content test :
                title test
                link home page test
                table title test
                table content test
    """
    def test_public_board(self, client):
        response = client.get('/publicBoard')
        data = response.data.decode()
        assert response.status_code == 200

        assert "<h1>Public board</h1>" in data

        assert """<a href="/">Home page</a>""" in data

        assert """<th scope="col">Club</th>""" in data
        assert """<th scope="col">Points</th>""" in data

        clubs = loadClubs()
        for club in clubs:
            assert club["name"] in data
            assert club["points"] in data
