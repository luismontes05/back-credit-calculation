from fastapi.security import HTTPBearer
from fastapi import Request
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        validate_token(auth.credentials)
