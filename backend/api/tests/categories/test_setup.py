from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from ...models import Category
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe", password="qwerasdf")
        self.dummy_category = Category.objects.create(name="dummy", owner=self.user)

        self.other_user = User.objects.create_user(
            username="janedoe", password="asdfxcvb"
        )
        self.other_user_category = Category.objects.create(
            name="other test", owner=self.other_user
        )

        self.category_data = {"name": "test"}

        self.client = APIClient()
        self.other_client = APIClient()
        self.anonymous_client = APIClient()

        token = AccessToken.for_user(user=self.user)
        other_token = AccessToken.for_user(user=self.other_user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token))
        self.other_client.credentials(
            HTTP_AUTHORIZATION="Bearer {}".format(other_token)
        )

        self.category_list_url = reverse("category-list")
        self.category_detail_url = reverse("category-detail", kwargs={"pk": 1})
        self.category_detail_url_does_not_exist = reverse(
            "category-detail", kwargs={"pk": 20}
        )

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
