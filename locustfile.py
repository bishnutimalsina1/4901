# Third party modules
from locust import HttpUser, between, task


class MyWebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def load_main(self):
        self.client.get("http://127.0.0.1:5000")

        # locust - f locustfile.py - -host =http://54.159.208.193
        # locust - f locustfile.py - -host =http://127.0.0.1:5000/