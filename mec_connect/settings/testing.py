from __future__ import annotations

import os

for k, v in {
    "ENVIRONMENT": "testing",
    "SECRET_KEY": "youshallnotpass",
    "DATABASE_URL": "postgres://postgres:postgres@localhost:5433/mecconnect-testing",
    "BROKER_URL": "redis://localhost:6380/0",
}.items():
    os.environ.setdefault(k, v)


from .default import *
