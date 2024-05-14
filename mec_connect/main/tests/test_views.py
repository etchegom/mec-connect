from __future__ import annotations

from django.urls import reverse


def test_webhook(client):
    resp = client.post(reverse("api:webhook"), {})
    assert resp.status_code == 200
    assert resp.json() == {}
