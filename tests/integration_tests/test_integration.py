from server import app
import pytest
from ..unit_tests.test_006_loading import TestLoading
from ..unit_tests.test_001_home import TestHome
from ..unit_tests.test_002_show_summary import TestShowSummary
from ..unit_tests.test_003_book_competition_club import TestBookCompetitionClub
from ..unit_tests.test_004_purchase_places import TestPurchasePlaces


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.mark.usefixtures("client")
class TestIntegration:
    """
    Integration Test

    :tests: test_integration
        :sequence of tests:
            test_load_clubs
            test_load_competitions
            test_home_page
            test_access_show_summary_with_right_email
            test_book_page_display
            test_with_places_number_and_points_below_the_available_one
            test_logout
    """
    def test_integration(self, client):
        TestLoading.test_load_clubs(self, client)
        TestLoading.test_load_competitions(self, client)
        TestHome.test_home_page(self, client)
        TestShowSummary.test_access_show_summary_with_right_email(self, client)
        TestBookCompetitionClub.test_book_page_display(self, client)
        TestPurchasePlaces\
            .test_with_places_number_and_points_below_the_available_one(
                self, client)
        TestHome.test_logout(self, client)
