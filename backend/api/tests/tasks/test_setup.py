from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from ...models import Category, Task
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe", password="qwerasdf")
        self.dummy_category = Category.objects.create(name="test", owner=self.user)
        self.dummy_task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            owner=self.user,
            status="not_started",
            category=self.dummy_category,
            due_date="2024-06-20T10:00:00Z",
        )

        self.other_user = User.objects.create_user(
            username="janedoe", password="asdfxcvb"
        )
        self.other_user_category = Category.objects.create(
            name="other test", owner=self.user
        )
        self.other_user_task = Task.objects.create(
            title="Test Task from another user",
            description="Test Description",
            owner=self.other_user,
            status="not_started",
            category=self.other_user_category,
            due_date="2024-06-21T10:00:00Z",
        )

        self.task_data = {
            "title": "Dummy task",
            "description": "This is the description for the dummy task.",
            "status": "not_started",
            "due_date": "2024-06-20T10:00:00Z",
            "category": "test",
        }

        self.client = APIClient()
        self.other_client = APIClient()
        self.anonymous_client = APIClient()

        token = AccessToken.for_user(user=self.user)
        other_token = AccessToken.for_user(user=self.other_user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token))
        self.other_client.credentials(
            HTTP_AUTHORIZATION="Bearer {}".format(other_token)
        )

        self.task_list_url = reverse("task-list")
        self.task_detail_url = reverse("task-detail", kwargs={"pk": 1})
        self.task_detail_url_does_not_exist = reverse("task-detail", kwargs={"pk": 20})

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
