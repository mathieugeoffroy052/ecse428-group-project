import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        self.client: APIClient = APIClient()

    def test_login_response_contains_has_seen_tutorial(self):
        response = self.client.post(
            reverse("login"),
            json.dumps(
                {"username": "johnsmith@example.com", "password": "password123"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("has_seen_tutorial" in response.json().keys())

    def test_user_sees_tutorial_on_first_login(self):
        new_user = get_user_model().objects.create_user(
            email="newuser@example.com", password="password123"
        )

        def new_user_login():
            return self.client.post(
                reverse("login"),
                json.dumps({"username": new_user.email, "password": "password123"}),
                content_type="application/json",
            )

        first_login_response = new_user_login()
        self.assertEqual(first_login_response.json()["has_seen_tutorial"], False)
        second_login_response = new_user_login()
        self.assertEqual(second_login_response.json()["has_seen_tutorial"], True)
