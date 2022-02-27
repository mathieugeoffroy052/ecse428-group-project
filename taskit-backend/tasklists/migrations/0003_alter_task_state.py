# Generated by Django 4.0.2 on 2022-02-24 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasklists', '0002_task_late_task_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.CharField(choices=[('NS', 'Not Started'), ('IP', 'In Progress'), ('C', 'Completed')], default=None, max_length=2, null=True),
        ),
    ]
