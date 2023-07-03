# Generated by Django 4.1.7 on 2023-07-03 08:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("Website", "0003_alter_announcement_notice"),
    ]

    operations = [
        migrations.CreateModel(
            name="Complaints",
            fields=[
                ("sno", models.AutoField(primary_key=True, serialize=False)),
                ("teamno", models.IntegerField()),
                ("idno", models.IntegerField()),
                ("roomno", models.IntegerField()),
                ("query", models.TextField(null=True)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
