from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.models.user import User
from src.services.auth import (
    authenticate_user,
    create_access_token_for_user,
    create_user,
)
from src.schemas.response import APIResponse
from sqlalchemy.exc import IntegrityError
from src.core.security import refresh_token_state, create_access_token
from src.services.send_email import send_email
from src.core.security import decode_access_token, mail_token, get_password_hash
from src.schemas.user import ForgotPasswordSchema

from src.core.config import settings


async def login_controller(form_data, db):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return APIResponse.error(code=401, message="Incorrect email or password")
    token = create_access_token_for_user(user)
    return APIResponse.success(data={"token": token})


async def register_controller(user_in, background_tasks, db):
    try:
        # Creation of user account
        user = create_user(db, email=user_in.email, password=user_in.password)

        # Sending account activation email
        if not user.is_active:
            token = create_access_token({"sub": user.email})
            params_email = {
                "email": user.email,
                "subject": "Account activation",
                "action": "activate_account",
                "language": user.lang,
                "params": {
                    "link": f"{settings.CLIENT_HOST + settings.CLIENT_ACCOUNT_ACTIVATION_URL + token}",
                    "app_ame": f"{settings.APP_NAME}",
                },
            }

            background_tasks.add_task(send_email, params_email)

        return APIResponse.success(
            message="Activation link sended successfully check your email"
        )
    except IntegrityError as e:
        return APIResponse.error(code=400, message="Already user exist.")


async def refresh_token_controller(refresh):
    if not refresh:
        return APIResponse.error(code=400, message="Refresh token required.")
    return APIResponse.success(
        message="Refresh token refresh successfully.",
        data=refresh_token_state(token=refresh),
    )


async def verify_account_controller(db, background_tasks, token):
    payload = await decode_access_token(token=token)

    if not payload:
        APIResponse.error(code=401, message="Token expire")

    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        return APIResponse.error(code=400, message="User not found.")

    user.is_active = True
    db.commit()
    db.refresh(user)

    # Sending of Welcome email and activation of “free” subscription plan
    if user:
        token = create_access_token({"sub": user.email})
        params_email = {
            "email": user.email,
            "subject": "Welcome",
            "action": "create_account",
            "language": user.lang,
            "params": {
                "username": f"{settings.CLIENT_HOST + settings.CLIENT_ACCOUNT_ACTIVATION_URL + token}",
                "credits": "",
                "app_ame": f"{settings.APP_NAME}",
            },
        }

        background_tasks.add_task(send_email, params_email)
    return APIResponse.success(message="Successfully activated")


async def forgot_password_controller(
    data: ForgotPasswordSchema,
    bg_task: BackgroundTasks,
    db: Session,
):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        token = mail_token(user)
        params_email = {
            "email": user.email,
            "subject": "Reset Password",
            "action": "reset_password",
            "language": user.lang,
            "params": {
                "link": f"{settings.CLIENT_HOST + settings.CLIENT_ACCOUNT_ACTIVATION_URL + token}",
                "username": f"{user.last_name} {user.first_name}",
                "app_ame": f"{settings.APP_NAME}",
            },
        }

        bg_task.add_task(send_email, params_email)

        return APIResponse.success(
            message="Reset token sended successfully your email check your email",
        )
    return APIResponse.error(code=404, message="User not found")


async def reset_password_controller(data, token, db):
    payload = await decode_access_token(token=token, db=db)
    if not payload:
        return APIResponse.error(code=400, message="Token expired.")
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        return APIResponse.error(code=404, message="User not found")

    user.password = get_password_hash(data.password)
    await user.save(db=db)

    return APIResponse.success(message="Password succesfully updated")
