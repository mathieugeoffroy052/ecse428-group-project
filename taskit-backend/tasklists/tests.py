from datetime import datetime, timedelta
from django.test import TestCase
from tasklists.models import Task
from accounts.models import User
from tasklists.views import view_all_tasks

class TestClass(TestCase):
        # Create your tests here.
    def test_view_all_task(self):
        user = User(email = "gingermuffin@gmail.com", password="GingerPower123")
        user.save()

        task1 = Task(owner=user, description = "eat food", due_datetime = datetime(2022,2,24,0,0,0,0), estimated_duration = timedelta(seconds=1800), weight = 50)
        task1.save()
        task2 = Task(owner=user, description = "drink all the milk", due_datetime = datetime(2022,2,4,0,0,0,0), estimated_duration = timedelta(seconds=1800), weight = 50)
        task2.save()

        all_tasks = [task1,task2]

        returned_tasks = view_all_tasks()

        self.assertEqual(all_tasks, returned_tasks)