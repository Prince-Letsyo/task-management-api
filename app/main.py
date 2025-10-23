from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core import  AppException
from app.config import config
from app.core.db import init_db
from app.routers import task_router, auth_router
from app.middlewares import (
    app_exception_handler,
    global_exception_handler,
    http_exception_handler,
    jwt_decoder,
    logging_middleware,
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield


app: FastAPI = FastAPI(
    title=config.app_name,
    license_info={"name": "MIT License"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ✅ FIXED: Use get_openapi() to avoid recursion
def custom_openapi() -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema: dict[str, Any] = get_openapi(  # pyright: ignore[reportExplicitAny]
        title=config.app_name,
        version=cast(str, config.env.get("VERSION", "1.0.0")),
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
    for path in openapi_schema["paths"].values():  # pyright: ignore[reportAny]
        for method in path.values():  # pyright: ignore[reportAny]
            method.setdefault(  # pyright: ignore[reportAny]
                "security", [{"BearerAuth": []}]
            )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=validation_exception_handler,  # pyright: ignore[reportArgumentType]
)
app.add_exception_handler(
    exc_class_or_status_code=HTTPException,
    handler=http_exception_handler,  # pyright: ignore[reportArgumentType]
)
app.add_exception_handler(
    exc_class_or_status_code=AppException,
    handler=app_exception_handler,  # pyright: ignore[reportArgumentType]
)
app.add_exception_handler(
    exc_class_or_status_code=Exception, handler=global_exception_handler
)

if config.enable_cors:
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
_ = app.middleware(middleware_type="http")(jwt_decoder)
_ = app.middleware(middleware_type="http")(logging_middleware)


app.include_router(router=auth_router)
app.include_router(router=task_router)


@app.get(path="/")
def index() -> dict[str, str]:
    return {"message": "Welcome to Task Management Api Project!"}
