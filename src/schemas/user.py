from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    profession: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profession: Optional[str] = None
    lang: Optional[str] = None

    class Config:
        from_attributes = True


class User(UserBase):
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserResponse(BaseModel):

    class Config:
        from_attributes = True


class PasswordUpdateSchema(BaseModel):
    password: str
    new_password: str
    confirm_password: str

    @field_validator("confirm_password")
    def verify_password_match(cls, v, values, **kwargs):
        password = values.get("new_password")

        if v != password:
            raise ValueError("The two passwords did not match.")

        return v


class PasswordResetSchema(BaseModel):
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def verify_password_match(cls, v, values, **kwargs):
        password = values.get("password")

        if v != password:
            raise ValueError("The two passwords did not match.")

        return v


class ForgotPasswordSchema(BaseModel):
    email: EmailStr
