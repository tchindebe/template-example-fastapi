from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

def raise_bad_request(message: str):
    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=message,
    )

def raise_unauthorized(message: str):
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=message,
    )