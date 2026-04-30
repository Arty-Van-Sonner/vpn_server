from fastapi import FastAPI

from vpn_server.api.routes.admin import router as admin_router
from vpn_server.api.routes.auth import router as auth_router
from vpn_server.core.config import settings
from vpn_server.db import seed_data

app = FastAPI(title=settings.app_name, version="0.1.0")

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)


@app.on_event("startup")
def on_startup() -> None:
    seed_data()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

