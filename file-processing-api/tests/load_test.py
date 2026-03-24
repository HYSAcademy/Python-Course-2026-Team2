from locust import HttpUser, task, between
from pathlib import Path

TEST_ZIP = Path(__file__).parent / "bigFile.zip"


class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def upload_archive(self):
        with TEST_ZIP.open("rb") as f:
            files = {"archives": f}
            self.client.post("/archives/upload", files=files)

    @task(1)
    def background_index(self):
        self.client.post("/archives/index/background")

    @task(3)
    def search(self):
        self.client.get("/archives/search", params={"query": "example", "top_k": 5})
