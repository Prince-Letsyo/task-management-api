from collections.abc import Awaitable
from typing import Any, Callable, cast
from fastapi import Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.types import Backend
from app.core.redis import SafeJsonCoder
from app.schemas import Task, User
from app.utils.auth import JWTPayload

# The generic type for the function being decorated
_Func = Callable[..., Any]  # pyright: ignore[reportExplicitAny]


def task_list_cache_key_builder(
    func: _Func,  # The function being decorated
    namespace: str,
    *,  # All remaining arguments must be passed as keyword arguments
    request: Request | None = None,
    response: Response | None = None,  # pyright: ignore[reportUnusedParameter]
    args: tuple[Any, ...],  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
    kwargs: dict[str, Any],  # pyright: ignore[reportExplicitAny, reportUnusedParameter]
) -> Awaitable[str] | str:
    """
    Builds unique cache keys based on query params for list endpoints.
    """
    # Defensive check, though Request should be present for list endpoints
    if request is None:
        return f"{namespace}:{func.__name__}"

    # The logic remains the same, but uses the Request object from kwargs/keyword args
    query = "&".join([f"{k}={v}" for k, v in sorted(request.query_params.items())])

    # We use request.url.path which should be safe.
    user = cast(JWTPayload, request.state.user)
    cache_key = f"{namespace}:{user.get("username")}:{request.url.path}"
    return f"{cache_key}?{query}" if query else f"{cache_key}"


def task_detail_cache_key_builder(
    func: _Func,  # The function being decorated
    namespace: str,
    *,  # All remaining arguments must be passed as keyword arguments
    request: Request | None = None,
    response: Response | None = None,  # pyright: ignore[reportUnusedParameter]
    args: tuple[Any, ...],  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
    kwargs: dict[str, Any],  # pyright: ignore[reportExplicitAny]
) -> Awaitable[str] | str:
    """
    Builds unique cache keys based on query params for list endpoints.
    """
    # Defensive check, though Request should be present for list endpoints
    if request is None:
        return f"{namespace}:{func.__name__}"

    # We use request.url.path which should be safe.
    user = cast(JWTPayload, request.state.user)
    task_id = cast(int, kwargs.get("task_id"))
    return f"{namespace}:{user.get("username")}:{task_id}"


async def cache_task_details(tasks: list[Task]):
    """Store individual task details in Redis."""
    redis: Backend = FastAPICache.get_backend()
    cache_key = FastAPICache.get_prefix()
    expire = FastAPICache.get_expire()
    for task in tasks:
        user: User = cast(User, task.user)
        username: str = user.username
        key = f"{cache_key}:task:detail:{username}:{task.id}"
        await redis.set(key, SafeJsonCoder.encode(task), expire=expire)

