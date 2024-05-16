# Generated by Django 5.0.5 on 2024-05-16 19:52
from __future__ import annotations

import uuid

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_alter_webhookevent_object_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="GristConfig",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("doc_id", models.CharField(max_length=32)),
                ("table_id", models.CharField(max_length=32)),
                ("enabled", models.BooleanField(default=True)),
                (
                    "object_type",
                    models.CharField(choices=[("projects.Project", "Project")], max_length=32),
                ),
                ("api_base_url", models.CharField(max_length=128)),
                ("api_key", models.CharField(max_length=64)),
            ],
            options={
                "verbose_name": "Grist configuration",
                "verbose_name_plural": "Grist configurations",
                "db_table": "gristconfig",
                "ordering": ("-created",),
            },
        ),
    ]
