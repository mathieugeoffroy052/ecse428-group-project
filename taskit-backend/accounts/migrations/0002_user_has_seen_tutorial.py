# Generated by Django 4.0.2 on 2022-03-21 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="has_seen_tutorial",
            field=models.BooleanField(default=False),
        ),
    ]