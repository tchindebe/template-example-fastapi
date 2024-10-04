import uuid
import sys
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Security, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.core.config import settings
from src.models.user import User
from src.core.database import get_db
from src.schemas.response import APIResponse
from src.core.exceptions import raise_unauthorized
from fastapi.responses import JSONResponse
from src.schemas.token import JwtTokenSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

REFRESH_COOKIE_NAME = "refresh"
SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"


def _get_utc_now():
    if sys.version_info >= (3, 2):
        # For Python 3.2 and later
        current_utc_time = datetime.now(timezone.utc)
    else:
        # For older versions of Python
        current_utc_time = datetime.utcnow()
    return current_utc_time


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(payload: dict, minutes: int | None = None) -> JwtTokenSchema:
    expire = _get_utc_now() + timedelta(
        minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM),
        payload=payload,
        expire=expire,
    )

    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except JWTError:
        return None


def get_current_user(
    db: Session = Depends(get_db), token: str = Security(oauth2_scheme)
) -> User:
    payload = decode_access_token(token)

    if not payload:
        return raise_unauthorized(message="Unauthorized")

    user_email: str = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()

    if user is None:
        return raise_unauthorized(message="Unauthorized")
    return user


def refresh_token_state(token: str):
    try:
        payload = decode_access_token(token)
        return {"token": create_access_token(payload=payload).token}
    except JWTError as ex:
        print(str(ex))
        return raise_unauthorized(message="Unauthorized")


def mail_token(user: User):
    """Return 10 minutes lifetime access_token"""
    payload = {SUB: str(user.email), JTI: str(uuid.uuid4()), IAT: _get_utc_now()}
    return create_access_token(payload=payload, minutes=10).token
