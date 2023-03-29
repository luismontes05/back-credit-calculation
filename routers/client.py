from fastapi import APIRouter, Depends, Path, Query, Body, Request
from fastapi.responses import  JSONResponse
from config.database import Session
from shemas.client import Client as ClientShema
from utils.jwt_manager import create_token
from pydantic import BaseModel
from passlib.context import CryptContext
from middlewares.jwt_beare import JWTBearer
from utils.jwt_manager import token_decode

client_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = Session()

@client_router.post('/api/client', tags=['client'], response_model=ClientShema, status_code=201, dependencies=[Depends(JWTBearer())])
def user_create(request: Request, Cliente: ClientShema) -> ClientShema:
    pass
