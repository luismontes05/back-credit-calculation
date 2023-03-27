from models.user import User as UserModel
from shemas.user import User
from fastapi.encoders import jsonable_encoder


class UserService():

    def __init__(self, db) -> None:
        self.db = db 

    def get_user_login(self,email):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        user = jsonable_encoder(result)
        return user
    
    def create_user(self, user: UserModel):
        new_user = UserModel(**user.dict())
        self.db.add(new_user)
        self.db.commit()
        new_user = self.db.query(UserModel).filter_by(id=new_user.id).first()
        return jsonable_encoder(new_user)
    
    def get_user_validate_token(self,id: int, status: bool):
        result = self.db.query(UserModel).filter(UserModel.id == id, UserModel.status == status).first()
        return result


