from ast import arg
import datetime
from django.forms import DurationField
from django.test import TestCase
from pytz import timezone
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from tasklists.models import Task
from django.urls import reverse
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
                state='NS'
            )
            self.t2 = Task.objects.create(
                owner=self.user, 
                description="Order takeout", 
                due_datetime="2022-03-01T22:30:30+00:00", 
                weight=20
            )
            self.client: APIClient = APIClient()

        def test_change_state(self):
            self.client.force_authenticate(user=self.user)
            pk = self.t1.pk
            response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps(
                {
                    "state":'C'
                }
            ),
            content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "description":"Make dinner", 
                    "due_datetime":"2022-03-01T17:30:30-05:00", 
                    "estimated_duration":None,
                    "weight":10,
                    "state":'C'
                },
            )

        def test_add_state(self):
            self.client.force_authenticate(user=self.user)
            pk = self.t2.pk
            response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps(
                {
                    "state":'NS'
                }
            ),
            content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "description":"Order takeout", 
                    "due_datetime":"2022-03-01T17:30:30-05:00",
                    "estimated_duration":None,
                    "weight":20,
                    "state":"NS"
                },
            )
        
        def test_remove_state(self):
            self.client.force_authenticate(user=self.user)
            pk = self.t1.pk
            response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps(
                {
                    "state":None
                }
            ),
            content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "description":"Make dinner", 
                    "due_datetime":"2022-03-01T17:30:30-05:00", 
                    "estimated_duration":None,
                    "weight":10,
                    "state":None
                },
            )

        def test_update_nonexisting_task(self):
            self.client.force_authenticate(user=self.user)
            pk = self.t2.pk+100
            response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps(
                {
                    "state":None
                }
            ),
            content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)

        def test_invalid_state(self):
            self.client.force_authenticate(user=self.user)
            pk = self.t1.pk
            response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps(
                {
                    "state":"abcd"
                }
            ),
            content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)
        
        def test_update_without_auth(self):
            pk = self.t1.pk
            response = self.client.put(
            reverse("update_state", args=[pk]),
            json.dumps(
                {
                    "state":"abcd"
                }
            ),
            content_type="application/json",
            )
            self.assertEqual(response.status_code, 403)