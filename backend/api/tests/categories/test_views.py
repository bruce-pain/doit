from .test_setup import TestSetUp
from rest_framework import status


class TestCategoryViews(TestSetUp):
    #################### Category creation ######################
    def test_anonymous_user_cannot_create_category(self):
        response = self.anonymous_client.post(
            self.category_list_url, self.category_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category(self):
        response = self.client.post(
            self.category_list_url, self.category_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.category_data["name"])

    def test_create_category_no_data(self):
        response = self.client.post(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_invalid_data(self):
        invalid_category_data = {
            "title": "invalid",
            "status": "undefined",
        }

        response = self.client.post(
            self.category_list_url, invalid_category_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ################ Category Retrieval ###################
    def test_anonymous_user_cannot_list_categorys(self):
        response = self.anonymous_client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_categorys(self):
        response = self.client.get(self.category_list_url)
        owner = [category["owner"] for category in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(set(owner)), 1)  # test if there is only one user category

    def test_anonymous_user_cannot_retrieve_category(self):
        response = self.anonymous_client.get(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_category(self):
        response = self.client.get(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["owner"], self.user.username
        )  # test if category belongs to current user

    def test_retrieve_category_does_not_exist(self):
        response = self.client.get(self.category_detail_url_does_not_exist)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_retrieve_other_user_category(self):
        response = self.other_client.get(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############## Category Update #################
    def test_update_category(self):
        data = {
            "name": "Updated category",
        }

        response = self.client.put(self.category_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["name"], self.dummy_category.name)

    ############ Category Delete ################
    def test_delete_category(self):
        response = self.client.delete(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
