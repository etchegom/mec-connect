# Generated by Django 5.0.5 on 2024-05-16 20:06
from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_gristconfig"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gristconfig",
            name="table_id",
        ),
    ]
