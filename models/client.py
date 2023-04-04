from config.database import Base
from sqlalchemy import Column, Integer, Float, String, Enum, DateTime, Boolean, Text, Numeric, Date, Interval,  ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

type_document_enum_option = Enum('CC','NIT','TI','PS','EXT')
sex_enum_option = Enum('MASCULINO','FEMENINO','OTRO')

class Client(Base):
    
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    type_document = Column(type_document_enum_option, nullable=False, default='CC')
    num_document = Column(String(20), nullable=False)
    document_from = Column(String(50))
    expedition_date_document = Column(Date)
    birth_date = Column(Date)
    birth_city = Column(String(50))
    sex = Column(sex_enum_option, default='OTRO')
    telephone_number_1 = Column(String(10))
    telephone_number_2 = Column(String(10))
    email = Column(String(100))
    city_residence = Column(String(50))
    civil_status = Column(Enum('SOLTERO','CASADO','U LIBRE', default='SOLTERO'))
    address_1 = Column(String(100), nullable=False)
    address_2 = Column(String(100))
    profession = Column(String(50))
    fixed_income_value = Column(Numeric(12, 2))
    other_income = Column(Numeric(12, 2))
    approved_credit = Column(Boolean)
    status_credit = Column(Boolean)
    maximum_amount = Column(Numeric(12, 2))
    minimum_amount = Column(Numeric(12, 2))
    risk_level = Column(Integer)
    habit_pay = Column(Integer)
    debt_value = Column(Numeric(12, 2))
    fixed_expenses = Column(Numeric(12, 2))
    data_credit_point = Column(Integer)
    account_bank = Column(String(50))
    type_account_bank = Column(String(20))
    observation = Column(Text)
    status = Column(Boolean)
    id_user_create = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    company = relationship("Company", backref="company")
    user = relationship("User", backref="user")


class TypeProperties(Base):

    __tablename__ = "type_properties"

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable=False)
    description = Column(String(100))
    status = Column(Boolean, nullable=False, default=True)

class PropertieClient(Base):

    __tablename__ = "propertie_client"

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable=False)
    description = Column(Text)
    value = Column(Float, nullable=False) 
    status_range = Column(Integer)
    status = Column(Boolean, default=True)
    type_properties_id = Column(Integer, ForeignKey('type_properties.id'))
    client_id = Column(Integer, ForeignKey('client.id')) 
    typeproperties = relationship("TypeProperties", backref="typeproperties")
    client = relationship("Client", backref="propertie_client")

class ReferencesClient(Base):

    __tablename__ = "references_client"

    id = Column(Integer, primary_key = True)
    frist_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    telephone_number = Column(String(10), nullable=False)
    type_reference = Column(Enum('PERSONAL','FAMILIAR','LABORAL', default='PERSONAL'))
    relation = Column(String(50), nullable=False) 
    create_date = Column(DateTime, default=datetime.now())
    update_date = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    client_reference = relationship("Client", backref="references_client") 





