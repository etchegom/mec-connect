import httpx
from pprint import pprint


api_base_url = "http://monespacecollectivite.localhost:8000/api"

resp = httpx.get(f"{api_base_url}/projects", follow_redirects=True)
assert resp.status_code == 200, f"status_code: {resp.status_code}"
pprint(resp.json())
