from fastapi import  Depends, status
from app.routers.base import CustomRouter
from app.schemas import AuthLogin, UserCreate
from app.services import AuthService, UserResponse
from app.core import get_auth_service


auth_router: CustomRouter = CustomRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/sign_up", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def sign_up(
    user_create: UserCreate,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> UserResponse:
    return await auth_service.sign_up(user_create)


@auth_router.post(path="/sign_in", response_model=UserResponse)
async def sign_in(
    login_user: AuthLogin,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> UserResponse:
    return await auth_service.log_in(
        username=login_user.username, password=login_user.password
    )
