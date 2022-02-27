"""
behave environment module for acceptance testing taskit project
"""

from rest_framework.test import APIClient as Client

def before_all(context):
    context.client = Client()

def before_scenario(context, _):
    context.response = None
    context.error = None
