"""
http http://localhost:8484/api/orgs Authorization:"Bearer XXX"
http http://localhost:8484/api/orgs/2/workspaces Authorization:"Bearer XXX"
http http://localhost:8484/api/workspaces/2/docs Authorization:"Bearer XXX"
http POST http://localhost:8484/api/workspaces/2/docs Authorization:"Bearer XXX" name=test
http http://localhost:8484/api/workspaces/2/docs Authorization:"Bearer XXX"
http http://localhost:8484/api/docs/77kBY7fjGaUXYkXtr4VbhM/tables Authorization:"Bearer XXX"
"""

from __future__ import annotations

from pprint import pprint

import httpx

api_key = "8df9b5f7bbddae96d757761ddfd9fdeaa6355814"
api_base_url = "http://localhost:8484/api"
api_headers = {"Authorization": f"Bearer {api_key}"}

org_id: str = None
workspace_id: str = None
doc_id: str = None

resp = httpx.get(
    f"{api_base_url}/orgs",
    headers=api_headers,
)
assert resp.status_code == 200
org_id = resp.json()[0]["id"]

print(f"Org ID: {org_id}")

resp = httpx.get(
    f"{api_base_url}/orgs/{org_id}/workspaces",
    headers=api_headers,
)
assert resp.status_code == 200

for workspace in resp.json():
    if workspace["name"] == "Sandbox":
        workspace_id = workspace["id"]
        break
assert workspace_id is not None

print(f"Workspace ID: {workspace_id}")

resp = httpx.get(
    f"{api_base_url}/workspaces/{workspace_id}",
    headers=api_headers,
)
assert resp.status_code == 200
docs = resp.json()["docs"]
for doc in docs:
    if doc["name"] == "Suivi MEC":
        doc_id = doc["id"]
        break

if doc_id is None:
    resp = httpx.post(
        f"{api_base_url}/workspaces/{workspace_id}/docs",
        headers=api_headers,
        json={
            "name": "Suivi MEC",
            "isPinned": True,
        },
    )
    assert resp.status_code == 200
    doc_id = resp.json()

    for col_id in ["A", "B", "C"]:
        httpx.delete(
            f"{api_base_url}/docs/{doc_id}/tables/1/columns/{col_id}",
            headers=api_headers,
        )

    resp = httpx.post(
        f"{api_base_url}/docs/{doc_id}/tables/1/columns",
        headers=api_headers,
        json={
            "columns": [
                {
                    "id": "project_id",
                    "fields": {"label": "ID", "type": "Text"},
                },
                {
                    "id": "project_name",
                    "fields": {"label": "Name", "type": "Text"},
                },
            ],
        },
    )
    assert resp.status_code == 200

print(f"doc ID: {doc_id}")

# resp = httpx.get(
#     f"{api_base_url}/docs/{doc_id}/tables",
#     headers=api_headers,
# )
# assert resp.status_code == 200
# print(resp.json())

resp = httpx.get(
    f"{api_base_url}/docs/{doc_id}/tables/1/records/?project_id=1",
    headers=api_headers,
)
assert resp.status_code == 200
pprint(resp.json()["records"])
