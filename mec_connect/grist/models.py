from __future__ import annotations

from django.db import models


class GristConfig(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        verbose_name = "Grist Configuration"
        verbose_name_plural = "Grist Configuration"

    def __str__(self):
        return self.key
