import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import task_router
from app.db.db import engine, Base
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV_MODE", "dev") == "prod":
        await init_db()
    yield


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(
    title="Task Management Api Project",
    version="1.0.0",
    description="A simple Task Management API built with FastAPI",
    contact={"name": "Prince Kumar", "email": "test@gm.com"},
    license_info={"name": "MIT License"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


app.include_router(task_router)


@app.get("/")
def index():
    return {"message": "Welcome to Task Management Api Project!"}
