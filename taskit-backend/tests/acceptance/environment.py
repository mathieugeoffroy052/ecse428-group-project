"""
behave environment module for acceptance testing taskit project
"""

def before_scenario(context, _):
    context.tasks = []
