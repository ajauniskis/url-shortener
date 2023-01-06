from fastapi import FastAPI

from app.api.endpoints.index import router as index_router


app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)

app.include_router(index_router)
