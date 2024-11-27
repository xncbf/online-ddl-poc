from locust import HttpUser, task, between, events
import random


class UserTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_all_deeplinks(self):
        # 랜덤하게 페이지네이션 테스트
        skip = random.randint(0, 1000)
        limit = random.randint(10, 100)
        self.client.get(f"/deeplinks/?skip={skip}&limit={limit}")
    
    @task
    def update_random_deeplink(self):
        with self.client.put("/deeplinks/random", catch_response=True) as response:
            if response.status_code == 404:
                response.success()
        
    
    @task
    def update_random_deeplink_with_lock(self):
        with self.client.put("/deeplinks/random-with-lock", catch_response=True) as response:
            if response.status_code == 404:
                response.success()
    