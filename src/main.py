from fastapi import FastAPI

from src.api import main_router

app = FastAPI(
    title="E-Journal API",
    version="0.1.0",
    root_path="/api",
)

app.include_router(main_router)
