from fastapi import FastAPI

from app.api.endpoints.index import router as index_router
from app.api.endpoints.router import api_router
from app.core import ProjectConfigParser, get_settings

settings = get_settings()
config = ProjectConfigParser()

app = FastAPI(
    title=settings.app_name
    if settings.env.lower() == "prod"
    else f"[{settings.env.upper()}] {settings.app_name}",
    description=config.description,
    version=config.version,
    contact=config.contacts,
    license_info=config.license,
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)

app.include_router(index_router)
app.include_router(api_router)
