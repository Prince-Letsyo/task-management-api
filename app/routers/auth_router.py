from fastapi import APIRouter, Depends, status
from app.schemas import AuthLogin, UserCreate
from app.services import AuthService, UserResponse
from app.dependencies import get_auth_service


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/sign_up", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def sign_up(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await auth_service.sign_up(user_create)


@auth_router.post("/sign_in", response_model=UserResponse)
async def sign_in(
    login_user: AuthLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await auth_service.log_in(
        username=login_user.username, password=login_user.password
    )
