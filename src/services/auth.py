from sqlalchemy.orm import Session

from src.core.security import verify_password, get_password_hash, create_access_token
from src.schemas.token import Token
from src.schemas.user import UserInDB
from src.models.user import User

from src.core.security import create_access_token


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session, email: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email, hashed_password=hashed_password, is_active=True, is_superuser=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_access_token_for_user(user: UserInDB):
    access_token = create_access_token(payload={"sub": user.email}).token
    return Token(access_token=access_token, token_type="bearer")
