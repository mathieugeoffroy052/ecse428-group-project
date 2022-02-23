from django.test import TestCase
from tasklists.models import Task
from accounts.models import User
from tasklists.views import view_all_tasks

class TestClass(TestCase):
        # Create your tests here.
    def test_view_all_task(self):
        user = User(email = "gingermuffin@gmail.com", password="GingerPower123")
        user.save()

        task1 = Task(owner="gingermuffin@gmail.com", description = "eat food", due_datetime = '2022-02-06', estimated_duration = 30, weight = 50)
        task1.save()
        task2 = Task(owner="gingermuffin@gmail.com", description = "drink all the milk", due_datetime = '2022-02-07', estimated_duration = 30, weight = 50)
        task2.save()

        all_tasks = [task1,task2]

        returned_tasks = view_all_tasks()

        self.assertEqual(all_tasks, returned_tasks)