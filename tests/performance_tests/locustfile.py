from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task()
    def home(self):
        self.client.get("/")

    @task()
    def show_summary(self):
        email = "john@simplylift.co"
        self.client.post("/showSummary", {"email": email})

    @task()
    def book_page(self):
        self.client.get("/book/" + "Spring Festival" + "/Simply Lift")

    @task()
    def purchase_places(self):
        self.client.post("/purchasePlaces", {"places": 1,
                                             "club": "Simply Lift",
                                             "competition": "Spring Festival"})

    @task()
    def public_board(self):
        self.client.get("/publicBoard")
