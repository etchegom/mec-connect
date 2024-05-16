from __future__ import annotations

import json
from typing import Any, Self

import httpx

from .models import GristConfig


def raise_on_4xx_5xx(response):
    response.raise_for_status()


class GristClient:
    api_key: str
    api_base_url: str
    doc_id: str

    def __init__(self, api_key: str, api_base_url: str, doc_id: str):
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.doc_id = doc_id

    @classmethod
    def from_config(cls, config: GristConfig) -> Self:
        return cls(
            api_key=config.api_key,
            api_base_url=config.api_base_url,
            doc_id=config.doc_id,
        )

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def client_factory(self) -> httpx.Client:
        return httpx.Client(
            headers=self.headers,
            base_url=self.api_base_url,
            event_hooks={"response": [raise_on_4xx_5xx]},
        )

    def get_records(self, table_id: str, filter: dict[str, Any]) -> dict[str, Any]:
        with self.client_factory() as client:
            resp = client.get(
                f"docs/{self.doc_id}/tables/{table_id}/records/",
                params={"filter": json.dumps(filter)},
            )
            return resp.json()["records"]

    def create_records(self, table_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        with self.client_factory() as client:
            resp = client.post(
                f"docs/{self.doc_id}/tables/{table_id}/records/",
                json={"records": [{"fields": fields}]},
            )
            return resp.json()