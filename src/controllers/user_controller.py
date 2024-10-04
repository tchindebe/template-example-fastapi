from src.models.user import User
from src.schemas.user import UserInDB
from src.schemas.response import APIResponse
from src.core.security import verify_password, get_password_hash


# Contrôleur de mise à jour le profil de l'utilisateur
async def update_profile_controller(db, user_data, current_user):
    db_user = db.query(User).filter(User.email == current_user.email).first()
    if db_user:
        for var, value in vars(user_data).items():
            setattr(db_user, var, value) if value else None
        db.commit()
        db.refresh(db_user)
        return APIResponse.success(
            message="Profile updated successfully",
            data={"user": UserInDB.from_orm(db_user)},
        )
    return APIResponse.error(code=404, message="User not found")


# Contrôleur de mise à jour le mot de passe de l'utilisateur
async def update_password_controller(db, user_password, current_user):
    db_user = db.query(User).filter(User.email == current_user.email).first()
    if db_user:
        if not verify_password(user_password.password, db_user.hashed_password):
            return APIResponse.error(code=400, message="Old password is incorrect.")
        db_user.password = get_password_hash(user_password.new_password)
        db.commit()
        db.refresh(db_user)
        return APIResponse.success(message="Password updated successfully")
    return APIResponse.error(code=404, message="User not found")


async def logout_controller(db, token):
    # payload = await decode_access_token(token=token, db=db)
    # black_listed = models.BlackListToken(
    #     id=payload["jti"], expire=datetime.utcfromtimestamp(payload["exp"])
    # )
    # await black_listed.save(db=db)

    return APIResponse.success(message="Succesfully logout")
