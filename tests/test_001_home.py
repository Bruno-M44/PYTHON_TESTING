from server import app
import codecs
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
            matching data with template index.html test
    """
    def test_home_page(self, client):
        response = client.get('/')
        data = response.data.decode()
        index_content = codecs.open("templates/index.html", 'r').read()
        assert response.status_code == 200
        assert data == index_content
