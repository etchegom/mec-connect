# Generated by Django 5.0.5 on 2024-05-24 15:15
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_gristconfig_table_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gristconfig",
            name="table_id",
            field=models.CharField(max_length=32),
        ),
    ]