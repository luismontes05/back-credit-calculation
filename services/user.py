from os import getenv
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from jwt import decode
from config.database import Session

class UserService():

    def __init__(self) -> None:
        self.db = self.db = Session()

    def get_user_login(self,email):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        user = jsonable_encoder(result)
        self.db.close()
        return user
    
    def create_user(self, user: UserModel, type_return='json'):

        if not self.validate_email_exists(user.email):
            new_user = UserModel(**user.dict())
            self.db.add(new_user)
            self.db.commit()
            new_user = self.db.query(UserModel).filter_by(id=new_user.id).first()
            self.db.close()
            if type_return == 'json':
                return jsonable_encoder(new_user)
            return new_user
        else:
            raise HTTPException(status_code=400, detail={"message": "The email entered already exists"})
    
    def get_user_validate_token(self,id: int, status: bool):
        result = self.db.query(UserModel).filter(UserModel.id == id, UserModel.status == status).first()
        self.db.close()
        return result
    
    def validate_email_exists(self, email: str):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        self.db.close()
        return result
    
    def validate_is_user_staf(self,token):
        
        data: dict = decode(token, key=getenv('SECRET'), algorithms=['HS256'])

        if data['type_user'] != getenv('USER_STAF'):
            raise HTTPException(status_code=401, detail={"message": "User invalid for operation"})

