"""
behave environment module for acceptance testing taskit project
"""
<<<<<<< HEAD
from django.test import Client
def before_all(context):
    context.client = Client()
    
def before_scenario(context, _):
    context.response = None
    context.error = None
    context.email = None
=======

from django.test import Client

def before_all(context):
    context.client = Client()

def before_scenario(context, _):
    context.response = None
    context.error = None
>>>>>>> d1e45e44487c2df3d218a288dcaafdebdfcb97b3
