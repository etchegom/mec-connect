from __future__ import annotations

from typing import Any, Self

from django.core.handlers.wsgi import WSGIRequest
from django.db import models

from mec_connect.utils.json import PrettyJSONEncoder
from mec_connect.utils.models import BaseModel

from .choices import WebhookEventStatus


class WebhookEvent(BaseModel):
    remote_ip = models.GenericIPAddressField(help_text="IP address of the request client.")
    headers = models.JSONField(default=dict)
    payload = models.JSONField(default=dict, encoder=PrettyJSONEncoder)

    status = models.CharField(
        max_length=32,
        choices=WebhookEventStatus.choices,
        default=WebhookEventStatus.PENDING,
        help_text="Whether or not the webhook event has been successfully processed",
    )

    exception = models.TextField(blank=True)
    traceback = models.TextField(
        blank=True, help_text="Traceback if an exception was thrown during processing"
    )

    class Meta:
        verbose_name = "Webhook Event"
        verbose_name_plural = "Webhook Events"
        db_table = "mec_webhookevent"
        ordering = ("-created",)

    @classmethod
    def create_from_request(cls, request: WSGIRequest, **kwargs: dict[str, Any]) -> Self:
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return cls.objects.create(remote_ip=ip, headers=dict(request.headers), **kwargs)
