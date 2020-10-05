
import random, json
from locust import HttpUser, task, between, TaskSet, User


class UserBehavior(HttpUser):
    min_wait = 5000
    max_wait = 9000

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.token = ""
        self.headers = {}

    def on_start(self):
        self.token = self.login()

        self.headers = {'Authorization': 'Token ' + self.token}

    def login(self):
        response = self.client.post("/v1/auth/login", data={'phoneNumber': '+666000666', 'password': 'dupadupa'})


    @task
    def index(self):
        self.client.get("/v1/me/profile", headers=self.headers)

