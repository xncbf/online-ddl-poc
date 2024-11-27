from locust import HttpUser, task, between
import random

class UserTest(HttpUser):
    wait_time = between(1, 3)
    
    @task(1)
    def get_all_deeplinks(self):
        # 랜덤하게 페이지네이션 테스트
        skip = random.randint(0, 1000)
        limit = random.randint(10, 100)
        self.client.get(f"/deeplinks/?skip={skip}&limit={limit}")
    
    @task(2)
    def update_random_deeplink(self):
        self.client.put("/deeplinks/random")
    
    @task(2)
    def update_random_deeplink_with_lock(self):
        self.client.put("/deeplinks/random-with-lock")
    