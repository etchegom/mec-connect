from __future__ import annotations

import httpx
from celery import shared_task
from celery.utils.log import get_task_logger

from .choices import WebhookEventStatus
from .grist import GristClient
from .models import GristConfig, WebhookEvent

logger = get_task_logger(__name__)


api_key = "8df9b5f7bbddae96d757761ddfd9fdeaa6355814"
api_base_url = "http://localhost:8484/api"
api_headers = {"Authorization": f"Bearer {api_key}"}
doc_id = "96uwtGo5ypmUGJ8BFk3YC2"


@shared_task
def sync_grist_table(event_id: int):
    try:
        event = WebhookEvent.objects.get(id=event_id)
    except WebhookEvent.DoesNotExist:
        logger.error(f"WebhookEvent with id={event_id} does not exist")
        return

    for grist_config in GristConfig.objects.filter(enabled=True, object_type=event.object_type):
        client = GristClient.from_config(grist_config)
        records = client.get_records(table_id="1", filter={"project_id": [event.object_id]})
        record_id = records[0]["id"] if records else None

        if record_id is None:
            client.create_records()
            resp = httpx.post(
                f"{api_base_url}/docs/{doc_id}/tables/1/records/",
                headers=api_headers,
                json={
                    "records": [
                        {
                            "fields": {
                                "project_id": event.object_id,
                                "project_name": event.payload["object"]["name"],
                            },
                        }
                    ]
                },
            )

        else:
            resp = httpx.patch(
                f"{api_base_url}/docs/{doc_id}/tables/1/records/",
                headers=api_headers,
                json={
                    "records": [
                        {
                            "id": record_id,
                            "fields": {
                                "project_name": event.payload["object"]["name"],
                            },
                        }
                    ]
                },
            )

    event.status = WebhookEventStatus.PROCESSED
    event.save()
