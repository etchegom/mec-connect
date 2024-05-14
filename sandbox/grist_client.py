"""
http http://localhost:8484/api/orgs Authorization:"Bearer XXX"
http http://localhost:8484/api/orgs/2/workspaces Authorization:"Bearer XXX"
http http://localhost:8484/api/workspaces/2/docs Authorization:"Bearer XXX"
http POST http://localhost:8484/api/workspaces/2/docs Authorization:"Bearer XXX" name=test
http http://localhost:8484/api/workspaces/2/docs Authorization:"Bearer XXX"
http http://localhost:8484/api/docs/77kBY7fjGaUXYkXtr4VbhM/tables Authorization:"Bearer XXX"
"""

from __future__ import annotations

import httpx

api_key = "8df9b5f7bbddae96d757761ddfd9fdeaa6355814"
api_base_url = "http://localhost:8484/api"
api_headers = {"Authorization": f"Bearer {api_key}"}

resp = httpx.get(f"{api_base_url}/orgs", headers=api_headers)
assert resp.status_code == 200
org_id = resp.json()[0]["id"]

resp = httpx.get(f"{api_base_url}/orgs/{org_id}/workspaces", headers=api_headers)
assert resp.status_code == 200

workspace_id = None
for workspace in resp.json():
    if workspace["name"] == "Sandbox":
        workspace_id = workspace["id"]
        break
assert workspace_id is not None

print("workspace_id:", workspace_id)

resp = httpx.get(f"{api_base_url}/workspaces/{workspace_id}", headers=api_headers)
assert resp.status_code == 200
docs = resp["docs"]
