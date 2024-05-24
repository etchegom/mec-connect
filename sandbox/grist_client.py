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


if doc_id is not None:
    resp = httpx.delete(
        f"{api_base_url}/docs/{doc_id}",
        headers=api_headers,
    )
    assert resp.status_code == 200

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
                "id": "id",
                "fields": {"label": "ID", "type": "Text"},
            },
            {
                "id": "name",
                "fields": {"label": "Nom du projet", "type": "Text"},
            },
            {
                "id": "context",
                "fields": {"label": "Contexte", "type": "Text"},
            },
            {
                "id": "additions",
                "fields": {"label": "Compléments", "type": "Text"},
            },
            {
                "id": "topics",
                "fields": {"label": "Thématique(s)", "type": "Text"},
            },
            {
                "id": "details",
                "fields": {"label": "Si autre, précisez", "type": "Text"},
            },
            {
                "id": "perimeter",
                "fields": {"label": "Périmètre", "type": "Text"},
            },
            {
                "id": "diagnostic_ANCT",
                "fields": {"label": "Diagnostic ANCT", "type": "Text"},
            },
            {
                "id": "attachment",
                "fields": {"label": "Pièce jointe", "type": "Text"},
            },
            {
                "id": "diagnostic_is_shared",
                "fields": {
                    "label": "Le diagnostic a-t-il été partagé à la commune ?",
                    "type": "Bool",
                },
            },
            {
                "id": "maturity",
                "fields": {"label": "Niveau de maturité", "type": "Text"},
            },
            {
                "id": "ownership",
                "fields": {"label": "Maître d'ouvrage", "type": "Text"},
            },
            {
                "id": "action",
                "fields": {"label": "Description de l'action", "type": "Text"},
            },
            {
                "id": "partners",
                "fields": {"label": "Partenaires", "type": "Text"},
            },
            {
                "id": "budget",
                "fields": {"label": "Budget prévisionnel", "type": "Numeric"},
            },
            {
                "id": "forecast_financing_plan",
                "fields": {
                    "label": "Plan de financement prévisionnel",
                    "type": "Text",
                },
            },
            {
                "id": "forecast_financing_plan_attachment",
                "fields": {"label": "PJ Financement prévisionnel", "type": "Text"},
            },
            {
                "id": "final_financing_plan",
                "fields": {
                    "label": "Plan de financement définitif",
                    "type": "Text",
                },
            },
            {
                "id": "forecast_financing_plan_attachment",
                "fields": {"label": "PJ Financement définitif", "type": "Text"},
            },
            {
                "id": "calendar",
                "fields": {"label": "Calendrier", "type": "Text"},
            },
            {
                "id": "administrative_procedures",
                "fields": {"label": "Procédures administratives", "type": "Text"},
            },
            {
                "id": "dependencies",
                "fields": {
                    "label": "Liens avec d'autres programmes et contrats",
                    "type": "Text",
                },
            },
            {
                "id": "evaluation_indicator",
                "fields": {
                    "label": "Indicateur de suivi et d'évaluation",
                    "type": "Text",
                },
            },
            {
                "id": "ecological_transition_compass",
                "fields": {
                    "label": "Boussole de transition ecologique",
                    "type": "Text",
                },
            },
            {
                "id": "verdict",
                "fields": {"label": "Verdict", "type": "Text"},
            },
            {
                "id": "grant_amount",
                "fields": {"label": "Montant de subvention", "type": "Numeric"},
            },
        ],
    },
)
assert resp.status_code == 200, resp.json()

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
