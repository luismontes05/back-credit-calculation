from config.database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from datetime import datetime

type_user_enum_option = Enum('staf','user')

class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    username = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(150), nullable=False)
    type_user = Column(type_user_enum_option, nullable=False, default='user')
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(Boolean, nullable=False, default=True)
