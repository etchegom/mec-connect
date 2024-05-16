from __future__ import annotations

from django.http import HttpRequest
from ninja import Router

from .models import WebhookEvent
from .schemas import WebhookEventSchema

router = Router()


@router.post("/webhook")
def webhook(request: HttpRequest, payload: WebhookEventSchema):
    d = payload.dict()
    obj = d.pop("object")
    d["object_id"] = obj["id"]

    event = WebhookEvent.create_from_request(request, **d)
    return {
        "id": event.id,
        "status": event.status,
    }
