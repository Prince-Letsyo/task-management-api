from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from app.schemas import UserCreate, User
from app.services import AuthService, UserResponse
from app.dependencies import get_auth_service


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/sign_up", response_class=UserResponse, status_code=status.HTTP_201_CREATED )
async def sign_up(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await auth_service.sign_up(user_create)




