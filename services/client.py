from models.client import Client as ClientModel, PropertieClient as PropertieClientModel, ReferencesClient as ReferencesClientModel
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from utils.jwt_manager import token_decode
from passlib.context import CryptContext


class ClientService():
    
    def __init__(self, db, request) -> None:
        
        self.db = db 
        #Obtiene los datos del header y decodifica el token para identificar el usuario
        self.request = request 
        self.data_user = token_decode(request)

    def validate_client_exist(self, type_document, num_document, company_id, email):

        #Valida que el usuario a crear no exista 
        result = self.db.query(ClientModel).filter(ClientModel.type_document == type_document, ClientModel.num_document == num_document, ClientModel.company_id == company_id).first()
        if result:
            raise HTTPException(status_code=401, detail={"message": "El cliente ya se encuentra registrado en la base de datos."})
        
        #Valida que el email ingresado no exista, ya que este sirve para el usuario y debe ser unico por empresa (company)
        result_user = self.db.query(UserModel).filter(UserModel.email == email, UserModel.company_id == company_id).first()
        if result_user:
            raise HTTPException(status_code=401, detail={"message": "El email ingresado para el cliente ya se encuentra registrado"})       
    
    def create_client(self, client: ClientModel):
        
        self.validate_client_exist(client.type_document,client.num_document,self.data_user['company_id'],client.email)

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        propertie_client = client.properties_client
        references_client = client.references_client
        del client.properties_client, client.references_client
   
        new_user = UserModel(username=client.first_name,
                             last_name=client.last_name,
                             email=client.email,
                             password=pwd_context.hash(client.num_document),
                             type_user='user',
                             company_id=self.data_user['company_id'])
        
        client.user_id = new_user.id
        client.id_user_create = self.data_user['id']
        client.company_id = self.data_user['company_id']
  
        new_client = ClientModel(**client.dict(),user=new_user)

        for propertie in propertie_client:
        
            new_propertie = PropertieClientModel(
                name=propertie.name,
                description=propertie.description,
                value=propertie.value,
                status_range=propertie.status_range,
                type_properties_id=propertie.type_properties_id,
                client=new_client
            )
            self.db.add(new_propertie)

        for reference in references_client:
        
            new_reference = ReferencesClientModel(

                frist_name=reference.frist_name,
                last_name=reference.last_name,
                telephone_number=reference.telephone_number,
                type_reference=reference.type_reference,
                relation=reference.relation,
                client_reference=new_client
            )
            self.db.add(new_reference)

        self.db.add(new_user)
        self.db.add(new_client)
        self.db.commit()
        new_client = self.db.query(ClientModel).filter(ClientModel.id == new_client.id).all()
        return jsonable_encoder(new_client)




        
    