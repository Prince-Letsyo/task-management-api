from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.schemas import UserCreate, User
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
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )
    return await auth_service.sign_in(username, password)
