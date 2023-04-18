from fastapi import APIRouter, Depends, Path, Query, Body, Request
from fastapi.responses import  JSONResponse
from services.user import UserService
from shemas.user import User
from utils.jwt_manager import create_token
from pydantic import BaseModel
from passlib.context import CryptContext
from middlewares.jwt_beare import JWTBearer
from utils.jwt_manager import token_decode


user_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserLoginResponse(BaseModel):
    message: str
    token: str 
    status: bool


@user_router.get('/api/login', tags=['auth'], response_model=UserLoginResponse, status_code=200)
def login(email, password):
    
    user = UserService().get_user_login(email)
    if user:
        if pwd_context.verify(password, user['password']):
            token: str = create_token(user)
            response = UserLoginResponse(message='user validate',token=token,status=True)
            return JSONResponse(status_code=200, content=response.dict())
  
    response = UserLoginResponse(message='Usuario o contraseña incorrecta',token='',status=False)
    return JSONResponse(status_code=401, content=response.dict())

@user_router.post('/api/user', tags=['user'], response_model=User, status_code=201, dependencies=[Depends(JWTBearer())])
def user_create(request: Request, user: User) -> User:
    
    '''
    PARA RECUEPERAR LA INFORMACION DEL USUARIO EN LA SESION, SE PUEDE REALIZAR DE LA SIGUIENTE MANERA
    data_user = token_decode(request)
    print(data_user)'''

    user.password = pwd_context.hash(user.password)
    new_user = UserService().create_user(user)
    return JSONResponse(status_code=201, content=new_user)