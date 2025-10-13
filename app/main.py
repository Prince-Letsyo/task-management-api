from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.db import init_db, AsyncSessionLocal
from app.config import config
from app.routers import task_router, auth_router
from app.dependencies import dependency_container
from app.middlewares import jwt_decoder, logging_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with AsyncSessionLocal() as session:
        await dependency_container.initialize(session)
        yield
        await session.close()

    yield
    await dependency_container.cleanup()


app = FastAPI(
    title=config.app_name,
    license_info={"name": "MIT License"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ✅ FIXED: Use get_openapi() to avoid recursion
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=config.app_name,
        version=config.env.get("VERSION"),
        description="A simple Task Management API built with FastAPI",
        contact={"name": "Prince Kumar", "email": "test@gm.com"},
        routes=app.routes,
    )

    # Add JWT Bearer auth definition
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: Bearer <token>",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.middleware("http")(jwt_decoder)
app.middleware("http")(logging_middleware)
if config.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def index():
    return {"message": "Welcome to Task Management Api Project!"}
