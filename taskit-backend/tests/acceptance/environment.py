"""
behave environment module for acceptance testing taskit project
"""

from rest_framework.test import APIClient as Client


def before_feature(context, _):
    context.client = Client()


def before_scenario(context, _):
    context.response = None
    context.error = None
    context.email = None
    context.user_pwd = {}
    context.client.credentials()
