# Generated by Django 4.1.7 on 2023-07-20 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Website", "0018_remove_room_submitted_team_submitted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="name",
            field=models.CharField(default="", max_length=20),
        ),
    ]
