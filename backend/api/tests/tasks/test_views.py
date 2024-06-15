from .test_setup import TestSetUp
from rest_framework import status


class TestTaskViews(TestSetUp):
    #################### Task creation ######################
    def test_anonymous_user_cannot_create_task(self):
        response = self.anonymous_client.post(
            self.task_list_url, self.task_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        response = self.client.post(self.task_list_url, self.task_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.task_data["title"])

    def test_create_task_no_data(self):
        response = self.client.post(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_invalid_data(self):
        invalid_task_data = {
            "name": "invalid",
            "status": "undefined",
        }

        response = self.client.post(
            self.task_list_url, invalid_task_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ################ Task Retrieval ###################
    def test_anonymous_user_cannot_list_tasks(self):
        response = self.anonymous_client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tasks(self):
        response = self.client.get(self.task_list_url)
        owner = [task["owner"] for task in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(set(owner)), 1)  # test if there is only one user task

    def test_anonymous_user_cannot_retrieve_task(self):
        response = self.anonymous_client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task(self):
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["owner"], self.user.username
        )  # test if task belongs to current user

    def test_retrieve_task_does_not_exist(self):
        response = self.client.get(self.task_detail_url_does_not_exist)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_retrieve_other_user_task(self):
        response = self.other_client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############## Task Update #################
    def test_update_task(self):
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "completed",
            "category": "test",
            "due_date": "2025-01-01T10:00:00Z",
        }

        response = self.client.put(self.task_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["title"], self.dummy_task.title)

    ############ Task Delete ################
    def test_delete_task(self):
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
