from __future__ import annotations

from datetime import datetime

from ninja import Schema


class WebhookEventObjectSchema(Schema):
    id: int
    name: str
    created_on: datetime
    updated_on: datetime


class WebhookEventSchema(Schema):
    topic: str
    object: WebhookEventObjectSchema
    object_type: str
    webhook_uuid: str
