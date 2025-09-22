from fastapi import FastAPI
from .api.endpoints import task_router
from .config import settings
from .core import create_db_and_tables
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Task Management Api Project",
    version=settings.version,
    description="A simple Task Management API built with FastAPI",
    contact={"name": "Prince Kumar", "email": "test@gm.com"},
    license_info={"name": "MIT License"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


app.include_router(task_router, prefix="/tasks", tags=["tasks"])


@app.get("/")
def index():
    return {"message": "Welcome to Task Management Api Project!"}
