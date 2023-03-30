from fastapi import APIRouter, Depends, Path, Query, Body, Request
from fastapi.responses import  JSONResponse
from config.database import Session
from shemas.client import Client as ClientShema
from passlib.context import CryptContext
from middlewares.jwt_beare import JWTBearer
from middlewares.validate_user_staf import ValidateUserStaf
from services.client import ClientService


client_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = Session()

@client_router.post('/api/client', tags=['client'], response_model=ClientShema, status_code=201, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def user_create(request: Request, new_client: ClientShema) -> dict:
    new_client = ClientService(db, request).create_client(new_client)
    return JSONResponse(status_code=201, content=new_client)
    
