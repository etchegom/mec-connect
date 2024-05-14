from __future__ import annotations

from ninja import Router

from .schemas import WebhookEventSchema

main_api_router = Router()


@main_api_router.post("/webhook")
def webhook(request, payload: WebhookEventSchema):
    pass
