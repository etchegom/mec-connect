from __future__ import annotations

from celery import shared_task
from celery.utils.log import get_task_logger

from .choices import WebhookEventStatus
from .grist import GristClient
from .models import GristConfig, WebhookEvent

logger = get_task_logger(__name__)


@shared_task
def sync_grist_table(event_id: int):
    try:
        event = WebhookEvent.objects.get(id=event_id)
    except WebhookEvent.DoesNotExist:
        logger.error(f"WebhookEvent with id={event_id} does not exist")
        return

    # TODO: move table_id to somewhere else, GristConfig?...
    table_id = "1"

    for grist_config in GristConfig.objects.filter(enabled=True, object_type=event.object_type):
        client = GristClient.from_config(grist_config)
        resp = client.get_records(
            table_id=table_id,
            filter={"project_id": [event.object_id]},
        )

        records = resp.json()["records"]

        if len(records):
            client.update_records(
                table_id="1",
                records={
                    records[0]["id"]: {
                        "project_name": event.payload["object"]["name"],
                    },
                },
            )
            continue

        client.create_records(
            table_id=table_id,
            records=[
                {"project_id": event.object_id},
                {"project_name": event.payload["object"]["name"]},
            ],
        )

    event.status = WebhookEventStatus.PROCESSED
    event.save()
