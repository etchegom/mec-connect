import httpx
from pprint import pprint


api_base_url = "http://monespacecollectivite.localhost:8000/api"


resp = httpx.post(
    f"{api_base_url}/token/",
    data={
        "username": "matthieu.etchegoyen@beta.gouv.fr",
        "password": "Password2!!",
    },
)
assert resp.status_code == 200, f"status_code: {resp.status_code}"
token = resp.json()["access"]

resp = httpx.get(
    f"{api_base_url}/projects/", headers={"Authorization": f"Bearer {token}"}
)
assert resp.status_code == 200, f"status_code: {resp.status_code}"
pprint(resp.json())
