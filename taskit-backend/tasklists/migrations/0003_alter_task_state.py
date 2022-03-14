# Generated by Django 4.0.2 on 2022-03-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasklists", "0002_task_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="state",
            field=models.CharField(
                choices=[
                    ("NS", "Not started"),
                    ("IP", "In progress"),
                    ("C", "Complete"),
                ],
                default="NS",
                max_length=2,
            ),
        ),
    ]
