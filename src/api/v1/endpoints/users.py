from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.schemas.response import APIResponse
from src.schemas.user import UserUpdate, PasswordUpdateSchema
from src.models.user import User
from src.core.security import get_current_user
from src.controllers.user_controller import (
    update_profile_controller,
    update_password_controller,
    logout_controller,
)

router = APIRouter()


@router.put("/profile", response_model=APIResponse)
async def update_user_profile(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    This route is used to update the logged in user profile information.
    - **first_name**: First Name.
    - **last_name**: Last Name.
    - **profession**: Profession.
    """
    return await update_profile_controller(db, user_data, current_user)


@router.put("/password-update", response_model=APIResponse)
async def update_user_password(
    user_password: PasswordUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    This route is used to update the password of the logged in user.
    - **password**: Current password.
    - **new_password**: New Password.
    - **confirm_password**: Confirm new password.
    """
    return await update_password_controller(db, user_password, current_user)


@router.post("/logout", response_model=APIResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    This route is used to log out the logged in user.
    """
    return await logout_controller(db, current_user)
