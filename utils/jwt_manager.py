import jwt  
import datetime
from os import getenv
from jwt import encode, decode
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from services.user import UserService
from config.database import Session


tiempo_expiracion = 30
fecha_expiracion = datetime.datetime.utcnow() + datetime.timedelta(minutes=tiempo_expiracion)

def create_token(data: dict):

    data["exp"] = fecha_expiracion
    token: str = encode(payload=data, key=getenv('SECRET'), algorithm="HS256")
    return token

def validate_token(token: str) -> dict:

    try:

        db = Session()
        data: dict = decode(token, key=getenv('SECRET'), algorithms=['HS256'])
        user = UserService(db).get_user_validate_token(id=data['id'], status=data['status'])
        if not user:
            raise HTTPException(status_code=401, detail={"message": "User invalid or User Inactive"})
        
        '''content = {
            "id": user.id,
            "username": user.username,
            "last_name": user.last_name,
            "type_user": user.type_user,
        }
        return JSONResponse(content=content, status_code=200)'''
    
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=401, detail={"message": "Token Expired"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail={"message": "Token is Invalid"})
    
def token_decode(request: Request) -> dict:
    token = request.headers['authorization'].split(" ")[1]
    data: dict = decode(token, key=getenv('SECRET'), algorithms=['HS256'])
    return data
