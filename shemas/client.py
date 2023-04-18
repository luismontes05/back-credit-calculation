from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Text
from enum import Enum
from datetime import date, datetime


class TypeDocument(str, Enum):
    value_a = 'CC'
    value_b = 'NIT'
    value_c = 'TI'
    value_d = 'PS'
    value_e = 'EXT'

class Sex(str, Enum):
    value_a = 'MASCULINO'
    value_b = 'FEMENINO'
    value_e = 'OTRO'

class CivilStatus(str, Enum):
    value_a = 'SOLTERO'
    value_b = 'CASADO'
    value_e = 'U LIBRE'

class TypeReference(str, Enum):
    value_a = 'PERSONAL'
    value_b = 'FAMILIAR'
    value_e = 'LABORAL'

class ReferencesClient(BaseModel):

    id: Optional[int] = None
    frist_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    telephone_number:  str = Field(..., min_length=7, max_length=10)
    type_reference: Optional[TypeReference] = Field(default='PERSONAL')
    relation: str = Field(..., min_length=3, max_length=50)
    status: bool = Field(default=True)
    client_id: Optional[int]

    class Config:
        schema_extra = {
            "example":{
                    'frist_name': 'Pedro',
                    'last_name': 'Gomez Gomez',
                    'telephone_number': '3100000000',
                    'type_reference': 'PERSONAL',
                    'relation': 'AMIGOS',
                    'status': True,
                    'client_id': 1
                }
            }

class PropertiesClient(BaseModel):
    
    id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=50)
    description: Text
    value: float
    status_range: int = Field(ge=1, le=10)
    status: bool = Field(default=True)
    type_properties_id: int
    client_id: Optional[int] = 1

    class Config:
        schema_extra = {
            "example":{
                    'name': 'CASA FINCA',
                    'description':'CASA FINCA UBICADA EN LA AV CONDINA',
                    'value':  100000000,
                    'status_range': 9,
                    'type_properties_id': 1,
                    'client_id': 1
                }
            }

class Client(BaseModel):

    id: Optional[int] = None
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    type_document: TypeDocument = Field(default="CC")
    num_document: str = Field(..., min_length=3, max_length=20)
    document_from: str = Field(..., min_length=5, max_length=50)
    expedition_date_document: Optional[date]
    birth_date: Optional[date]
    birth_city: Optional[str] = Field(..., min_length=3, max_length=50)
    sex: Optional[Sex]
    telephone_number_1: Optional[str] = Field(...,max_length=10)
    telephone_number_2: Optional[str] = Field(...,max_length=10)
    email: EmailStr
    city_residence: Optional[str] = Field(...,max_length=50)
    civil_status: Optional[CivilStatus]
    address_1: str = Field(..., max_length=100)
    address_2: Optional[str] = Field(..., max_length=100)
    profession: Optional[str] = Field(..., max_length=50)
    fixed_income_value: Optional[float]
    other_income: Optional[float]
    approved_credit: Optional[bool]
    status_credit: Optional[bool]
    maximum_amount: Optional[float]
    minimum_amount: Optional[float]
    risk_level: Optional[int] = Field(ge=1, le=10)
    habit_pay: Optional[int] = Field(ge=1, le=10)
    debt_value: Optional[float]
    fixed_expenses: Optional[float]
    data_credit_point: Optional[int] = Field(ge=1, le=1000)
    account_bank: Optional[str] = Field(..., max_length=50)
    type_account_bank: Optional[str] = Field(...,max_length=20)
    observation: Optional[Text]
    status: Optional[bool]
    id_user_create: Optional[int]
    company_id: Optional[int]
    user_id: Optional[int]
    references_client: List[ReferencesClient]
    properties_client: List[PropertiesClient]

    class Config:
        schema_extra = {
            "example":{
                'first_name': 'Pedro',
                'last_name': 'Gomez Gomez',
                'type_document': 'CC',
                'num_document': '12345678',
                'document_from': 'PEREIRA',
                'expedition_date_document': '2011-07-25',
                'birth_date': '1993-07-05',
                'birth_city': 'PEREIRA',
                'sex': 'MASCULINO',
                'telephone_number_1': '3100000000',
                'telephone_number_2': '3100000000',
                'email': 'example@example.com',
                'city_residence': 'PEREIRA',
                'civil_status': 'SOLTERO',
                'address_1': 'MZ 1 CS 1 SECTOR 1',
                'address_2': 'BARRIO PARQUE INDUSTRIAL - PEREIRA',
                'profession': 'INGENIERO',
                'fixed_income_value': '300000000',
                'other_income': '100000000',
                'approved_credit': False,
                'status_credit': False,
                'maximum_amount': '300000000',
                'minimum_amount': '100000000',
                'risk_level': 1,
                'habit_pay': 1,
                'debt_value': '350000000',
                'fixed_expenses': '15000000',
                'data_credit_point': 500,
                'account_bank': '123456790',
                'type_account_bank': 'AHORROS',
                'observation': 'CLIENTE DE PRUEBA',
                'status': True,
                'references_client': [                    
                    {
                        'frist_name': 'Pedro',
                        'last_name': 'Gomez Gomez',
                        'telephone_number': '3100000000',
                        'type_reference': 'PERSONAL',
                        'relation': 'AMIGOS',
                        'status': True,
                        'client_id': 1
                    }
                ],
                'properties_client':[
                    {
                        'name': 'CASA FINCA',
                        'description':'CASA FINCA UBICADA EN LA AV CONDINA',
                        'value':  100000000,
                        'status_range': 9,
                        'type_properties_id': 1
                    }
                ]
            }
        }

class ClientUpdate(BaseModel):

    first_name: Optional[str] = Field(..., min_length=3, max_length=50)
    last_name: Optional[str] = Field(..., min_length=3, max_length=50)
    type_document: Optional[TypeDocument] = Field(default="CC")
    num_document: Optional[str] = Field(..., min_length=3, max_length=20)
    document_from: Optional[str] = Field(..., min_length=5, max_length=50)
    expedition_date_document: Optional[date]
    birth_date: Optional[date]
    birth_city: Optional[str] = Field(..., min_length=3, max_length=50)
    sex: Optional[Sex]
    telephone_number_1: Optional[str] = Field(..., min_length=7, max_length=50)
    telephone_number_2: Optional[str] = Field(..., min_length=7, max_length=50)
    email: Optional[EmailStr]
    city_residence: Optional[str] = Field(..., min_length=3, max_length=50)
    civil_status: Optional[CivilStatus]
    address_1: Optional[str] = Field(..., max_length=100)
    address_2: Optional[str] = Field(..., max_length=100)
    profession: Optional[str] = Field(..., min_length=3, max_length=50)
    fixed_income_value: Optional[float]
    other_income: Optional[float]
    approved_credit: Optional[bool]
    status_credit: Optional[bool]
    maximum_amount: Optional[float]
    minimum_amount: Optional[float]
    risk_level: Optional[int] = Field(ge=1, le=10)
    habit_pay: Optional[int] = Field(ge=1, le=10)
    debt_value: Optional[float]
    fixed_expenses: Optional[float]
    data_credit_point: Optional[int] = Field(ge=1, le=1000)
    account_bank: Optional[str] = Field(..., min_length=3, max_length=50)
    type_account_bank: Optional[str] = Field(..., min_length=3, max_length=20)
    observation: Optional[Text]
    status: Optional[bool]

    class Config:
        schema_extra = {
            "example":{
                'first_name': 'Pedro',
                'last_name': 'Gomez Gomez',
                'type_document': 'CC',
                'num_document': '12345678',
                'document_from': 'PEREIRA',
                'expedition_date_document': '2011-07-25',
                'birth_date': '1993-07-05',
                'birth_city': 'PEREIRA',
                'sex': 'MASCULINO',
                'telephone_number_1': '3100000000',
                'telephone_number_2': '3100000000',
                'email': 'example@example.com',
                'city_residence': 'PEREIRA',
                'civil_status': 'SOLTERO',
                'address_1': 'MZ 1 CS 1 SECTOR 1',
                'address_2': 'BARRIO PARQUE INDUSTRIAL - PEREIRA',
                'profession': 'INGENIERO',
                'fixed_income_value': '300000000',
                'other_income': '100000000',
                'approved_credit': False,
                'status_credit': False,
                'maximum_amount': '300000000',
                'minimum_amount': '100000000',
                'risk_level': 1,
                'habit_pay': 1,
                'debt_value': '350000000',
                'fixed_expenses': '15000000',
                'data_credit_point': 500,
                'account_bank': '123456790',
                'type_account_bank': 'AHORROS',
                'observation': 'CLIENTE DE PRUEBA',
                'status': True
            }
        }
