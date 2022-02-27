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
        response = response.json()
        self.assertEqual(response.get("description"), "eat chocolate")
        self.assertEqual(response.get("due_datetime"), None)
        self.assertEqual(response.get("estimated_duration"), None)
        self.assertEqual(response.get("estimated_weight"), None)

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
        self.assertEqual(response.status_code, 401)

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
        response = response.json()[0]
        self.assertEqual(response.get("description"), "eat chocolate")
        self.assertEqual(response.get("due_datetime"), None)
        self.assertEqual(response.get("estimated_duration"), None)
        self.assertEqual(response.get("estimated_weight"), None)

    def test_get_urgency_normal(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) + timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
            }
        )
        result = task.get_urgency()
        self.assertEqual(result[0], False)
        self.assertAlmostEqual(
            round(result[1], 3), round(math.atan(1 / 2) * 2 / math.pi, 3)
        )  # comparing floats

    def test_get_urgency_late(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) - timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
            }
        )
        result = task.get_urgency()
        self.assertEqual(result[0], True)
        self.assertAlmostEqual(
            round(result[1], 3), round(math.atan(1 * 2) * 2 / math.pi, 3)
        )  # slight time difference

    def test_get_urgency_no_due_date(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": None,
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
            }
        )
        result = task.get_urgency()
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], None)

    def test_get_urgency_no_estimated_duration(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) - timedelta(hours=2),
                "estimated_duration": None,
                "weight": 100,
            }
        )
        result = task.get_urgency()
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], None)

    def test_get_weight_normal(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) + timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
            }
        )
        result = task.get_weight()
        self.assertAlmostEqual(
            result, math.atan(100 / 100) * 2 / math.pi
        )  # comparing floats

    def test_get_weight_no_weight(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) + timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": None,
            }
        )
        self.assertEqual(task.get_weight(), None)

    def test_get_priority_normal(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) + timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
            }
        )
        result = task.get_priority()
        expected_result = (
            math.atan(100 / 100) * 2 / math.pi + math.atan(1 / 2) * 2 / math.pi * 2 / 3
        )
        self.assertEqual(result[0], False)
        self.assertAlmostEqual(
            round(result[1], 3), round(expected_result, 3)
        )  # slight time difference

    def test_get_priority_late(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) - timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
            }
        )
        result = task.get_priority()
        expected_result = (
            math.atan(100 / 100) * 2 / math.pi + math.atan(2 * 1) * 2 / math.pi * 2 / 3
        )
        self.assertEqual(result[0], True)
        self.assertAlmostEqual(
            round(result[1], 3), round(expected_result, 3)
        )  # slight time difference

    def test_get_priority_no_urgency(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": None,
                "estimated_duration": None,
                "weight": 100,
            }
        )
        result = task.get_priority()
        self.assertEqual(result[0], False)
        self.assertAlmostEqual(result[1], None)  # slight time difference

    def test_get_priority_no_weight(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) + timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": None,
            }
        )
        result = task.get_priority()
        self.assertEqual(result[0], False)
        self.assertAlmostEqual(result[1], None)  # slight time difference
