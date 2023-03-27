from config.database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, Text
from datetime import datetime

type_document_enum_option = Enum('nit','cc')

class Company(Base):

    __tablename__ = "comapny"

    id = Column(Integer, primary_key = True)
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    company_name = Column(String(100), nullable=False)
    name_peron_contact = Column(String(120), nullable=False)
    telephone_person_contact = Column(String(10), nullable=False)
    telephone_person_contact_2 = Column(String(10), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    email = Column(String(100), nullable=True)
    config = Column(Text, nullable=True)
    city = Column(String(50), nullable=True)
    document =  Column(String(20), nullable=True)
    type_document = Column(type_document_enum_option, nullable=False, default='nit')


