from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from tasklists.models import Task
from django.urls import reverse
import json

User = get_user_model()


class TaskListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        self.client: APIClient = APIClient()

    def test_create_task_with_all_fields(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps(
                {
                    "description": "eat chocolate",
                    "due_datetime": "2022-02-26T01:34:41+00:00",
                    "estimated_duration": "03:00:00",
                    "weight": 10000,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "description": "eat chocolate",
                "due_datetime": "2022-02-25T20:34:41-05:00",
                "estimated_duration": "03:00:00",
                "weight": 10000,
            },
        )

    def test_create_task_with_just_a_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps(
                {
                    "description": "eat chocolate",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "description": "eat chocolate",
                "due_datetime": None,
                "estimated_duration": None,
                "weight": None,
            },
        )

    def test_create_task_with_a_blank_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps({"description": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "description": ["This field may not be blank."],
            },
        )

    def test_create_task_without_a_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "description": ["This field is required."],
            },
        )

    def test_create_task_without_being_authenticated(self):
        response = self.client.post(
            reverse("task_list"),
            json.dumps({"description": "eat chocolate"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_getting_all_tasks(self):
        self.client.force_authenticate(user=self.user)
        Task.objects.create(owner=self.user, description="eat chocolate")
        other_user = User.objects.create_user(
            email="other@example.com", password="password123"
        )
        Task.objects.create(owner=other_user, description="eat toothpaste")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "description": "eat chocolate",
                    "due_datetime": None,
                    "estimated_duration": None,
                    "weight": None,
                }
            ],
        )
    
    def test_deleting_task(self):
        self.client.force_authenticate(user=self.user)
        choccy_task = Task.objects.create(owner=self.user, description="eat chocolate")
        chips_task = Task.objects.create(owner=self.user, description="eat chips")
        response = self.client.delete(reverse("task_list"), {"id": choccy_task.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "Task deleted"})

    def test_deleting_task_without_being_authenticated(self):
        response = self.client.delete(reverse("task_list"), {"id": 42})
        self.assertEqual(response.status_code, 403)
    
    def test_deleting_nonexistent_task(self):
        self.client.force_authenticate(user=self.user)
        id = 42
        # Make absolutely sure there's no task with the given ID
        existing_tasks = Task.objects.filter(id=id)
        if existing_tasks:
            existing_tasks.first().delete()
        response = self.client.delete(reverse("task_list"), {"id": id})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Not found"})
