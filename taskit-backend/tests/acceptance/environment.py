"""
behave environment module for acceptance testing taskit project
"""
<<<<<<< HEAD
from django.test import Client
def before_all(context):
    context.client = Client()
    
=======

from rest_framework.test import APIClient as Client


def before_all(context):
    context.client = Client()


>>>>>>> c1010146b449dad55448439ccea2a49788bbd550
def before_scenario(context, _):
    context.response = None
    context.error = None
    context.email = None
