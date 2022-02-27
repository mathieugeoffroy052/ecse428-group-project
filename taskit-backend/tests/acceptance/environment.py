"""
behave environment module for acceptance testing taskit project
"""
from django.test import Client
def before_all(context):
    context.client = Client()
    
def before_scenario(context, _):
    context.response = None
    context.error = None
    context.email = None
