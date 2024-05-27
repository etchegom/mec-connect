# Generated by Django 5.0.5 on 2024-05-27 11:16
from __future__ import annotations

import functools

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_alter_gristconfig_table_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="gristconfig",
            name="columns",
            field=models.JSONField(
                default=dict,
                encoder=functools.partial(
                    django.core.serializers.json.DjangoJSONEncoder,
                    *(),
                    **{"indent": 2, "sort_keys": True},
                ),
            ),
        ),
    ]
