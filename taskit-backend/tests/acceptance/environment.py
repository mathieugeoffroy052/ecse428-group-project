"""
behave environment module for acceptance testing taskit project
"""
# from django.test.utils import setup_test_environment
from django.test import Client
def before_all(context):
    context.client = Client()
#     setup_test_environment()
def before_scenario(context, _):
    context.response = None
    context.error = None
    context.username = None