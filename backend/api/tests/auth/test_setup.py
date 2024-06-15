from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")

        self.user_data = {"username": "frankdoe", "password": "qwerasdf"}

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
