from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime



class EnumTypeUser(str, Enum):
    value_a = 'staf'
    value_b = 'user'


class User(BaseModel):

    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=10, max_length=50)
    email: EmailStr = Field(default="email@dominio.com")
    password: str
    type_user: EnumTypeUser
    create_date: datetime = Field(default=datetime.now())
    status: bool = Field(default=True)

    class Config:
        schema_extra = {
            "example":{
                'username': 'Pedro',
                'last_name': 'Gomez Gomez',
                'email': 'example@example.com',
                'password': 'secret',
                'type_user': 'user'
            }
        }


