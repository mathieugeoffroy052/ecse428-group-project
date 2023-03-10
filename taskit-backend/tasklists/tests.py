from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from tasklists.models import Task, TaskList
from django.urls import reverse
from datetime import datetime, timedelta, timezone
import math
import json

User = get_user_model()


class UpdateTaskListNameTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        self.t1 = TaskList.objects.create(
            owner=self.user,
            list_name="food",
        )
        self.t2 = TaskList.objects.create(
            owner=self.user,
            list_name="school",
        )
        self.client: APIClient = APIClient()

    def test_edit_name(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t1.pk
        response = self.client.put(
            reverse("edit_name", args=[pk]),
            json.dumps({"list_name": "buy food"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["list_name"], "buy food")

    def test_update_nonexisting_tasklist(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t2.pk + 100
        response = self.client.put(
            reverse("edit_name", args=[pk]),
            json.dumps({"list_name": None}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Task List Not found")

    def test_invalid_task_list_name(self):
        self.client.force_authenticate(user=self.user)
        pk = self.t1.pk
        response = self.client.put(
            reverse("edit_name", args=[pk]),
            json.dumps({"list_name": None}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid list name")

    def test_edit_name_without_auth(self):
        pk = self.t1.pk
        response = self.client.put(
            reverse("edit_name", args=[pk]),
            json.dumps({"list_name": "code"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)


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
            notes="aNote",
        )
        self.t2 = Task.objects.create(
            owner=self.user,
            description="Order takeout",
            due_datetime="2022-03-01T22:30:30+00:00",
            weight=20,
            notes="Second note",
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
        self.assertEqual(
            datetime.fromisoformat(response.json()["due_datetime"]),
            datetime.fromisoformat(self.t1.due_datetime),
        )
        self.assertEqual(response.json()["weight"], 10)
        self.assertEqual(response.json()["state"], "C")
        self.assertEqual(response.json()["notes"], "aNote")

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
        self.assertEqual(
            datetime.fromisoformat(response.json()["due_datetime"]),
            datetime.fromisoformat(self.t2.due_datetime),
        )
        self.assertEqual(response.json()["weight"], 20)
        self.assertEqual(response.json()["state"], "NS")
        self.assertEqual(response.json()["notes"], "Second note")

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


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        self.client: APIClient = APIClient()

    def test_create_task_with_all_fields(self):
        self.client.force_authenticate(user=self.user)
        task_list = TaskList.objects.create_task_list(self.user, "Food")
        response = self.client.post(
            reverse("task"),
            json.dumps(
                {
                    "description": "eat chocolate",
                    "due_datetime": "2022-02-26T01:34:41+00:00",
                    "estimated_duration": "03:00:00",
                    "weight": 10000,
                    "notes": "aNote",
                    "tasklist": task_list.id,
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
                "notes": "aNote",
                "tasklist": task_list.id,
            },
            response.json()["data"],
        )

    def test_create_task_with_just_a_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task"),
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
                "notes": "",
            },
            response.json()["data"],
        )

    def test_create_task_with_a_blank_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task"),
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
            reverse("task"),
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

    def test_create_task_without_a_note(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task"),
            json.dumps(
                {
                    "description": "Test",
                    "due_datetime": "2022-02-26T01:34:41+00:00",
                    "estimated_duration": "04:00:00",
                    "weight": 10000,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(
            {
                "description": "Test",
                "due_datetime": "2022-02-25T20:34:41-05:00",
                "estimated_duration": "04:00:00",
                "weight": 10000,
                "notes": "",
            },
            response.json()["data"],
        )

    def test_create_task_without_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task"),
            json.dumps(
                {
                    "description": "Test",
                    "due_datetime": "2022-02-26T01:34:41+00:00",
                    "estimated_duration": "04:00:00",
                    "weight": 10000,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(
            {
                "description": "Test",
                "due_datetime": "2022-02-25T20:34:41-05:00",
                "estimated_duration": "04:00:00",
                "weight": 10000,
                "tasklist": None,
            },
            response.json()["data"],
        )

    def test_create_task_invalid_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task"),
            json.dumps(
                {
                    "description": "Test",
                    "due_datetime": "2022-02-26T01:34:41+00:00",
                    "estimated_duration": "04:00:00",
                    "weight": 10000,
                    "tasklist": -1,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["tasklist"], ['Invalid pk "-1" - object does not exist.']
        )

    def test_create_task_without_being_authenticated(self):
        response = self.client.post(
            reverse("task"),
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
        response = self.client.get(reverse("task"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 1)
        response = response.json()[0]
        self.assertEqual(response.get("description"), "eat chocolate")
        self.assertEqual(response.get("due_datetime"), None)
        self.assertEqual(response.get("estimated_duration"), None)
        self.assertEqual(response.get("estimated_weight"), None)
        self.assertEqual(response.get("notes"), "")

    def test_get_urgency_normal(self):
        task = Task.objects.create(
            **{
                "owner": self.user,
                "description": "eat chocolate",
                "due_datetime": datetime.now(timezone.utc) + timedelta(hours=2),
                "estimated_duration": timedelta(days=0, hours=1),
                "weight": 100,
                "notes": "New note",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
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
                "notes": "New notes!",
            }
        )
        result = task.get_priority()
        self.assertEqual(result[0], False)
        self.assertAlmostEqual(result[1], None)  # slight time difference

    def test_deleting_task(self):
        self.client.force_authenticate(user=self.user)
        choccy_task = Task.objects.create(owner=self.user, description="eat chocolate")
        chips_task = Task.objects.create(owner=self.user, description="eat chips")
        response = self.client.delete(reverse("task"), {"id": choccy_task.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "Task deleted"})

    def test_deleting_task_without_being_authenticated(self):
        response = self.client.delete(reverse("task"), {"id": 42})
        self.assertEqual(response.status_code, 401)

    def test_deleting_nonexistent_task(self):
        self.client.force_authenticate(user=self.user)
        id = 42
        # Make absolutely sure there's no task with the given ID
        existing_tasks = Task.objects.filter(id=id)
        if existing_tasks:
            existing_tasks.first().delete()
        response = self.client.delete(reverse("task"), {"id": id})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Not found"})


class EditTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        self.task = Task.objects.create(
            owner=self.user,
            description="Make dinner",
            due_datetime="2022-03-01T22:30:30+00:00",
            weight=10,
            state="NS",
            notes="aNote",
        )
        self.client: APIClient = APIClient()

    def test_edit_task(self):
        self.client.force_authenticate(user=self.user)
        edited_task = {
            "id": 1,
            "description": "eat banana",
            "due_datetime": "2040-02-26T01:34:41+00:00",
            "estimated_duration": "09:00:00",
            "weight": 1,
            "state": "IP",
            "notes": "hmmmm delicious",
        }
        response = self.client.put(
            reverse("task"),
            json.dumps(edited_task),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["data"]["description"], edited_task["description"]
        )
        self.assertEqual(
            datetime.fromisoformat(response.json()["data"]["due_datetime"]),
            datetime.fromisoformat(edited_task["due_datetime"]),
        )
        self.assertEqual(
            response.json()["data"]["estimated_duration"],
            edited_task["estimated_duration"],
        )
        self.assertEqual(response.json()["data"]["weight"], edited_task["weight"])
        self.assertEqual(response.json()["data"]["state"], edited_task["state"])
        self.assertEqual(response.json()["data"]["notes"], edited_task["notes"])

    def test_edit_task_without_being_authenticated(self):
        edited_task = {
            "id": 1,
            "description": None,
            "due_datetime": "2040-02-26T01:34:41+00:00",
            "estimated_duration": "09:00:00",
            "weight": 1,
            "state": "IP",
            "notes": "hmmmm delicious",
        }
        response = self.client.put(
            reverse("task"),
            json.dumps(edited_task),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_edit_nonexistent_task(self):
        self.client.force_authenticate(user=self.user)
        edited_task = {
            "id": 10,
            "description": "eat banana",
            "due_datetime": "2040-02-26T01:34:41+00:00",
            "estimated_duration": "09:00:00",
            "weight": 1,
            "state": "IP",
            "notes": "hmmmm delicious",
        }
        response = self.client.put(
            reverse("task"),
            json.dumps(edited_task),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Not found"})


class TaskListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="johnsmith@example.com", password="password123"
        )
        self.client: APIClient = APIClient()

    def test_getting_all_task_lists(self):
        self.client.force_authenticate(user=self.user)
        TaskList.objects.create(owner=self.user, list_name="consume")
        other_user = User.objects.create_user(
            email="other@example.com", password="password123"
        )
        TaskList.objects.create(owner=other_user, list_name="eject")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 1)
        response = response.json()[0]
        self.assertEqual(response.get("list_name"), "consume")

    def test_create_task_list_with_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps({"list_name": "School Work"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(
            {"list_name": "School Work"},
            response.json()["data"],
        )
        self.assertEqual(response.json()["success"], "Task list created succesfully.")

    def test_create_task_list_with_blank_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps({"list_name": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "list_name": ["This field may not be blank."],
            },
        )

    def test_create_task_list_without_a_name(self):
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
                "list_name": ["This field is required."],
            },
        )

    def test_create_task_list_name_too_long(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("task_list"),
            json.dumps({"list_name": "I am choosing a very very very long name"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "list_name": ["Ensure this field has no more than 35 characters."],
            },
        )

    def test_create_task_list_without_being_authenticated(self):
        response = self.client.post(
            reverse("task_list"),
            json.dumps({"list_name": "School Work"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_task_list(self):
        self.client.force_authenticate(user=self.user)
        taskListSchool = TaskList.objects.create(
            owner=self.user, list_name="School Work"
        )
        response = self.client.delete(reverse("task_list"), {"id": taskListSchool.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], "Task list deleted successfully.")

    def test_delete_nonexistent_task_list(self):
        self.client.force_authenticate(user=self.user)
        fakeId = 101
        existing_task_lists = TaskList.objects.filter(id=fakeId)
        if existing_task_lists:
            existing_task_lists.first().delete()
        response = self.client.delete(reverse("task_list"), {"id": fakeId})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Not found.")

    def test_delete_task_list_without_being_authenticated(self):
        response = self.client.delete(reverse("task_list"), {"id": 101})
        self.assertEqual(response.status_code, 401)
