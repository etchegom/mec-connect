from __future__ import annotations

from .choices import ObjectType, WebhookEventStatus
from .models import WebhookEvent
from .tasks import sync_grist_table


def on_webhook_event_commit(event: WebhookEvent) -> None:
    if event.status != WebhookEventStatus.PENDING:
        return

    match event.object_type:
        case ObjectType.PROJECT:
            sync_grist_table.delay(event.id)
        case _:
            pass
