from .test_setup import TestSetUp
from rest_framework import status


class TestAuthViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_created_user_can_get_token(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.token_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_created_user_cannot_get_token(self):
        response = self.client.post(self.token_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_created_user_can_refresh_token(self):
        self.client.post(self.register_url, self.user_data, format="json")
        token_response = self.client.post(self.token_url, self.user_data, format="json")

        refresh_token = {"refresh": token_response.data["refresh"]}

        response = self.client.post(
            self.token_refresh_url, refresh_token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
