from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.auth_controller import (
    login_controller,
    refresh_token_controller,
    register_controller,
    verify_account_controller,
    forgot_password_controller,
    reset_password_controller,
)
from src.core.database import get_db
from src.schemas.response import APIResponse
from src.schemas.user import UserCreate, ForgotPasswordSchema, PasswordResetSchema

router = APIRouter()


@router.post("/login", response_model=APIResponse)
async def account_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    This route allows login to the user account.
    - **username**: User's email address.
    - **password**: Password.
    """
    return await login_controller(form_data, db)


@router.post("/register", response_model=APIResponse)
async def account_register(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    This route allows the creation of user accounts.
    - **email**: User's email address.
    - **password**: Password.
    """
    return await register_controller(user_in, background_tasks, db)


@router.post("/refresh", response_model=APIResponse)
async def refresh(refresh: str = None):
    return refresh_token_controller(refresh)


@router.get("/verify", response_model=APIResponse)
async def verify_and_activate_account(
    token: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    This route allows to activate the user account after its creation.
    - **token**: Token received by email.
    """
    return await verify_account_controller(db, background_tasks, token)


@router.post("/forgot-password", response_model=APIResponse)
async def forgot_password(
    data: ForgotPasswordSchema,
    bg_task: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    This route allows to generate a link with a token allowing to reset the password of the non-logged in user.
    - **email**: User's email address.
    """
    return await forgot_password_controller(data, bg_task, db)


@router.post("/password-reset", response_model=APIResponse)
async def password_reset(
    token: str,
    data: PasswordResetSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    This route is used to update the password of the non-logged in user.
    - **token**: Token received by email.
    - **password**: New Password.
    - **confirm_password**: Confirming new password.
    """
    return await reset_password_controller(data, token, db)
