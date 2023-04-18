from fastapi.security import HTTPBearer
from fastapi import Request
from utils.jwt_manager import validate_token
from services.user import UserService


class ValidateUserStaf(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        userService = UserService()
        userService.validate_is_user_staf(token=auth.credentials)