from typing import cast

from fastapi.background import BackgroundTasks
from pydantic import NameEmail
from app.config import config
from app.services.auth_service import (
    ActivateUserAccountResponse,
    ActivationEmail,
    RestPassword,
    UserResponse,
)


from fastapi import Depends, Request, status
from app.routers.base import CustomRouter
from app.schemas import AccessToken, AuthLogin, UserCreate
from app.services import AuthService
from app.core import get_auth_service
from app.utils import email_service, is_valid_url


auth_router: CustomRouter = CustomRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/sign-up", response_model=dict[str, str], status_code=status.HTTP_201_CREATED
)
async def sign_up(
    request: Request,
    user_create: UserCreate,
    background: BackgroundTasks,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> dict[str, str]:
    activate_user_response: ActivateUserAccountResponse = await auth_service.sign_up(
        user_create=user_create
    )
    FRONTEND_URL = cast(str, config.env.get("FRONTEND_URL", ""))
    link = request.url_for("activate_account")
    activation_link: str = (
        f"{FRONTEND_URL+link.path if is_valid_url(url=FRONTEND_URL) else link}?token={activate_user_response.token.token}"
    )
    background.add_task(
        func=email_service.send_activate_email,
        activate_user_response=activate_user_response.model_dump(),
        activation_link=activation_link,
    )
    return {
        "message": "User created successfully. Please check your email to activate your account."
    }


@auth_router.post(path="/sign-in", response_model=UserResponse)
async def sign_in(
    login_user: AuthLogin,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> UserResponse:
    return await auth_service.log_in(
        username=login_user.username, password=login_user.password
    )


@auth_router.post(path="/access", response_model=AccessToken)
async def get_access_token(
    token_string: str,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
):
    return await auth_service.get_access_token(token_string=token_string)


@auth_router.get(
    path="/activate-account",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    name="activate_account",
)
async def activate_account(
    token: str,
    background: BackgroundTasks,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
):
    user = await auth_service.activate_account(token=token)
    background.add_task(
        func=email_service.send_welcome_email,
        to_email=NameEmail(name=user.username, email=user.email),
    )
    return {"message": "Account activated successfully. You can now log in."}


@auth_router.post(
    path="/send-activation-email",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    name="send_activation_email",
)
async def send_activation_email(
    request: Request,
    user_email: ActivationEmail,
    background: BackgroundTasks,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
):
    activate_user_response: ActivateUserAccountResponse = (
        await auth_service.send_activation_email(email=user_email.email)
    )
    FRONTEND_URL = cast(str, config.env.get("FRONTEND_URL", ""))
    link = request.url_for("activate_account")
    activation_link: str = (
        f"{FRONTEND_URL+link.path if is_valid_url(url=FRONTEND_URL) else link}?token={activate_user_response.token.token}"
    )
    background.add_task(
        func=email_service.send_activate_email,
        activate_user_response=activate_user_response.model_dump(),
        activation_link=activation_link,
    )
    return {"message": "Activation email sent successfully. Please check your email."}


@auth_router.post(
    path="/request-password-reset",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    name="request_password_reset",
)
async def request_password_reset(
    request: Request,
    user_email: ActivationEmail,
    background: BackgroundTasks,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
):
    activate_user_response = await auth_service.request_password_reset(email=user_email.email)
    FRONTEND_URL = cast(str, config.env.get("FRONTEND_URL", ""))
    link = request.url_for("reset_password")
    reset_link: str = (
        f"{FRONTEND_URL+link.path if is_valid_url(url=FRONTEND_URL) else link}?token={activate_user_response.token.token}"
    )
    background.add_task(
        func=email_service.send_password_reset_email,
        to_email=NameEmail(name=activate_user_response.username, email=activate_user_response.email),
        reset_link=reset_link, 
    )
    return {
        "message": "A password reset link has been sent to your email."
    }


@auth_router.post(
    path="/reset-password",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    name="reset_password",
)
async def reset_password(
    token: str,
    rest_password: RestPassword,
    auth_service: AuthService = Depends(
        dependency=get_auth_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
):
    _=await auth_service.password_reset(token=token, rest_password=rest_password)
    return {"message": "Password has been reset successfully."}