from __future__ import annotations

from ninja import NinjaAPI

from mec_connect.main.views import main_api_router

api = NinjaAPI(
    title="MEC Connect API",
    version="1.0.0",
    description="API for MEC Connect",
    openapi_url="/openapi.json",
    docs_url="/docs",
    urls_namespace="api",
)
api.add_router("", main_api_router, tags=["MEC"])
