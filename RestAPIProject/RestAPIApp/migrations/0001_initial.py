# Generated by Django 4.1.13 on 2024-09-28 14:30

import RestAPIApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Inventory_Management",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "quality",
                    models.IntegerField(
                        validators=[RestAPIApp.models.validation_quality]
                    ),
                ),
            ],
        ),
    ]
