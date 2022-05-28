from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def purchase(self):
        self.client.post(
            "/purchasePlaces",
            {"club": "Simply Lift", "competition": "Spring Festival", "places": 3},
        )

    @task
    def logout(self):
        self.client.get("/logout")
