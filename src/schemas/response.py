from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder


class APIResponse(BaseModel):
    code: int
    status: str
    message: Optional[str] = None
    data: Optional[dict] = None

    @staticmethod
    def success(code: int = 200, data: dict = None, message: str = None):
        return APIResponse(
            code=code, status="success", message=message, data=jsonable_encoder(data)
        )

    @staticmethod
    def error(code: int, message: str):
        return APIResponse(code=code, status="error", message=message)
