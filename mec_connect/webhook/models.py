from __future__ import annotations

from typing import Any, Self

from django.core.handlers.wsgi import WSGIRequest
from django.db import models

from mec_connect.models import BaseModel
from mec_connect.utils import PrettyJSONEncoder

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
        abstract = True

    @classmethod
    def create_from_request(cls, request: WSGIRequest, **kwarg: dict[str, Any]) -> Self:
        """Create and process an Event given a Django request object."""
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return cls.objects.create(remote_ip=ip, headers=dict(request.headers), **kwarg)
