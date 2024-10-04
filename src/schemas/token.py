from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime