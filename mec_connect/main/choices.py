from __future__ import annotations

from django.db import models


class WebhookEventStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSED = "PROCESSED", "Processed"
    INVALID = "INVALID", "Invalid"
    FAILED = "FAILED", "Failed"
