from fastapi import APIRouter, Depends, Path, Query, Body, Request
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import Session
from shemas.client import Client as ClientShema, ReferencesClient as Referencesshema, PropertiesClient as PropertiesShecma, ClientUpdate as ClientShemaUpdate
from passlib.context import CryptContext
from middlewares.jwt_beare import JWTBearer
from middlewares.validate_user_staf import ValidateUserStaf
from services.client import ClientService


client_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = Session()


@client_router.get('/api/client', tags=['client'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def get_client(request: Request,id: int=0,  num_document: str=''):
    data_client = ClientService(db, request).get_client(id, num_document)
    return JSONResponse(status_code=200, content=jsonable_encoder(data_client))


@client_router.get('/api/client/references', tags=['client'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def get_reference(request: Request,id: int=0,  client_id: int=0):
    data_reference = ClientService(db, request).get_reference(id, client_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(data_reference))


@client_router.get('/api/client/properties', tags=['client'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def get_propertie(request: Request,id: int=0,  client_id: int=0):
    data_propertie = ClientService(db, request).get_propertie(id, client_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(data_propertie))


@client_router.post('/api/client', tags=['client'], response_model=ClientShema, status_code=201, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def create_client(request: Request, new_client: ClientShema) -> dict:
    new_client = ClientService(db, request).create_client(new_client)
    return JSONResponse(status_code=201, content=jsonable_encoder(new_client))


@client_router.post('/api/client/references', tags=['client'], response_model=Referencesshema, status_code=201, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def create_reference(request: Request, new_reference: Referencesshema) -> Referencesshema:
    new_reference = ClientService(db, request).create_reference(new_reference)
    return JSONResponse(status_code=201, content=jsonable_encoder(new_reference))


@client_router.post('/api/client/properties', tags=['client'], response_model=PropertiesShecma, status_code=201, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def create_propertie(request: Request, new_propertie: PropertiesShecma) -> PropertiesShecma:
    new_propertie = ClientService(db, request).create_propertie(new_propertie)
    return JSONResponse(status_code=201, content=jsonable_encoder(new_propertie))

@client_router.put('/api/client/{id}', tags=['client'], response_model=ClientShemaUpdate, status_code=200, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def update_client(id: int, request: Request, update_client: ClientShemaUpdate) -> dict:
    result = ClientService(db, request).update_client(id, update_client)
    return JSONResponse(status_code=200, content=result)

@client_router.put('/api/client/references/{id}', tags=['client'], response_model=Referencesshema, status_code=200, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def update_reference(id: int, request: Request, update_reference: Referencesshema) -> dict:
    result = ClientService(db, request).update_reference(id, update_reference)
    return JSONResponse(status_code=200, content=result)

@client_router.put('/api/client/properties/{id}', tags=['client'], response_model=PropertiesShecma, status_code=200, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def update_propertie(id: int, request: Request, update_propertie: PropertiesShecma) -> dict:
    result = ClientService(db, request).update_propertie(id, update_propertie)
    return JSONResponse(status_code=200, content=result)

@client_router.delete('/api/client/references/{id}', tags=['client'], response_model=Referencesshema, status_code=200, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def delete_reference(id: int, request: Request) -> dict:
    result = ClientService(db, request).delete_reference(id)
    return JSONResponse(status_code=200, content=result)

@client_router.delete('/api/client/properties/{id}', tags=['client'], response_model=PropertiesShecma, status_code=200, dependencies=[Depends(JWTBearer()), Depends(ValidateUserStaf())])
def delete_propertie(id: int, request: Request) -> dict:
    result = ClientService(db, request).delete_propertie(id)
    return JSONResponse(status_code=200, content=result)



