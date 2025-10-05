from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.config.db import init_db
from app.routers import task_router
from app.services import decode_access_token
from app.utils import ENV_MODE
from app.routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if ENV_MODE == "prod":
        await init_db()
    yield


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


@app.middleware("http")
async def jwt_decoder(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        payload = decode_access_token(token.split(" ")[1])
        request.state.user = {
            "username": payload.get("username"),
            "email": payload.get("email"),
        }
    else:
        request.state.user = None
    return await call_next(request)


app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def index():
    return {"message": "Welcome to Task Management Api Project!"}
