# Generated by Django 4.1.7 on 2023-07-20 18:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Website", "0019_alter_student_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="remarks",
            field=models.CharField(default="", max_length=500),
        ),
    ]
