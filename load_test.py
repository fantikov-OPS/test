from locust import HttpUser, between, task

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def write_data(self):
        self.client.post(
            "/write_data",
            json={"phone": "375259160655", "address": "123 Main St."}
        )

    @task
    def check_data(self):
        self.client.get("/check_data?phone=%2B71234567890")