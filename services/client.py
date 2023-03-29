from models.client import Client as ClientModel
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from utils.jwt_manager import token_decode


class ClientService():
    
    def __init__(self, db, request) -> None:
        
        self.db = db 
        #Obtiene los datos del header y decodifica el token para identificar el usuario
        self.request = request 
        self.data_user = token_decode(request)

    def create_client(self, client: ClientModel):
        pass
        
    