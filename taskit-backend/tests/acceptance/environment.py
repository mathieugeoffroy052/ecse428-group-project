"""
behave environment module for acceptance testing taskit project
"""
@before_all
def before_all(context):
    context.tasks = []