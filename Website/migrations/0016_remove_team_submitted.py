# Generated by Django 4.1.7 on 2023-07-17 10:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Website", "0015_team_submitted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="submitted",
        ),
    ]
