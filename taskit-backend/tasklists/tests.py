from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from tasklists.models import Task
from django.urls import reverse
from datetime import datetime, timedelta, timezone
import math
import json

User = get_user_model()


class UpdateTaskStateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])"""
        self.t1 = Task.objects.create(
            owner=self.user,
            description="Make dinner",
            due_datetime="2022-03-01T22:30:30+00:00",
            weight=10,
            state="NS",
        )
        self.t2 = Task.objects.create(
            owner=self.user,
            description="Order takeout",
            due_datetime="2022-03-01T22:30:30+00:00",
            weight=20,
        )
        self.client: APIClient = APIClient()

    def test_change_state(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t1.pk
        response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps({"state": "C"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Make dinner")
        self.assertEqual(response.json()["due_datetime"], "2022-03-01T17:30:30-05:00")
        self.assertEqual(response.json()["weight"], 10)
        self.assertEqual(response.json()["state"], "C")

    def test_add_state(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t2.pk
        response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps({"state": "NS"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Order takeout")
        self.assertEqual(response.json()["due_datetime"], "2022-03-01T17:30:30-05:00")
        self.assertEqual(response.json()["weight"], 20)
        self.assertEqual(response.json()["state"], "NS")

    def test_remove_state(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t1.pk
        response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps({"state": None}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Make dinner")
        self.assertEqual(response.json()["due_datetime"], "2022-03-01T17:30:30-05:00")
        self.assertEqual(response.json()["weight"], 10)
        self.assertEqual(response.json()["state"], None)

    def test_update_nonexisting_task(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t2.pk + 100
        response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps({"state": None}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_state(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t1.pk
        response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps({"state": "abcd"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_without_auth(self):
        pk = self.t1.pk
        response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps({"state": "NS"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)




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
        self.assertDictContainsSubset(
            {
                "description": "eat chocolate",
                "due_datetime": "2022-02-25T20:34:41-05:00",
                "estimated_duration": "03:00:00",
                "weight": 10000,
            },
            response.json(),
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
        self.assertDictContainsSubset(
            {
                "description": "eat chocolate",
                "due_datetime": None,
                "estimated_duration": None,
                "weight": None,
            },
            response.json(),
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

        self.assertEqual(len(response.json()),1)
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

    def test_deleting_task(self):
        self.client.force_authenticate(user=self.user)
        choccy_task = Task.objects.create(owner=self.user, description="eat chocolate")
        chips_task = Task.objects.create(owner=self.user, description="eat chips")
        response = self.client.delete(reverse("task_list"), {"id": choccy_task.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "Task deleted"})

    def test_deleting_task_without_being_authenticated(self):
        response = self.client.delete(reverse("task_list"), {"id": 42})
        self.assertEqual(response.status_code, 401)

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
