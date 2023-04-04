from models.client import Client as ClientModel, PropertieClient as PropertieClientModel, ReferencesClient as ReferencesClientModel
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from utils.jwt_manager import token_decode
from passlib.context import CryptContext
from datetime import datetime


class ClientService():
    
    def __init__(self, db, request) -> None:
        
        self.db = db 
        #Obtiene los datos del header y decodifica el token para identificar el usuario
        self.request = request 
        self.data_user = token_decode(request)


    def get_client(self,id: int=0, num_document: str=''):
        
        if id !=0:
            client = self.db.query(ClientModel).filter(ClientModel.id == id).first()
        elif num_document != '':
            client = self.db.query(ClientModel).filter(ClientModel.num_document == num_document, ClientModel.company_id == self.data_user['company_id']).first()
        else:
            client = self.db.query(ClientModel).filter(ClientModel.company_id == self.data_user['company_id']).all()
   
        if not client:
            raise HTTPException(status_code=404, detail={"message": "Los datos del cliente ingresado no existe"}) 

        if id != 0 or  num_document != '':
            client.user
            client.propertie_client
            client.references_client
        elif id == 0:
            list_client = []
            for cl in client:
                cl.user
                cl.propertie_client
                cl.references_client
                list_client.append(cl)
            
            client = list_client

        return  client
    

    def get_reference(self, id: int=0, client_id: int=0):

        if id !=0:
            reference = self.db.query(ReferencesClientModel).filter(ReferencesClientModel.id == id).first()
        else: 
            reference = self.db.query(ReferencesClientModel).filter(ReferencesClientModel.client_id == client_id).all()

        if not reference:
            raise HTTPException(status_code=404, detail={"message": "No existen referencias asociadas al cliente"}) 
        
        return reference
    

    def get_propertie(self, id: int=0, client_id: int=0):

        if id !=0:
            propertie = self.db.query(PropertieClientModel).filter(PropertieClientModel.id == id).first()
        else: 
            propertie = self.db.query(PropertieClientModel).filter(PropertieClientModel.client_id == client_id).all()

        if not propertie:
            raise HTTPException(status_code=404, detail={"message": "No existen propiedades asociadas al cliente"}) 
        
        return propertie


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
        return new_client


    def create_reference(self, reference: ReferencesClientModel):
        
        client = self.get_client(id=reference.client_id)        
        new_reference = ReferencesClientModel(**reference.dict(),client_reference=client)
        self.db.add(new_reference)
        self.db.commit()
        new_reference = self.db.query(ReferencesClientModel).filter(ReferencesClientModel.id == new_reference.id).all()
        return new_reference
    

    def create_propertie(self, propertie: PropertieClientModel):
        
        client = self.get_client(id=propertie.client_id)        
        new_propertie = PropertieClientModel(**propertie.dict(),client=client)
        self.db.add(new_propertie)
        self.db.commit()
        new_propertie = self.db.query(PropertieClientModel).filter(PropertieClientModel.id == new_propertie.id).all()
        return new_propertie


    def update_client(self,id, client: ClientModel):

        current_client = self.get_client(id)

        if current_client.type_document != client.type_document or current_client.num_document != client.num_document or current_client.email != client.email:
            self.validate_client_exist(client.type_document, client.num_document, self.data_user['company_id'], client.email)
        
        current_client.last_update = datetime.now()
        current_client.first_name = client.first_name
        current_client.last_name = client.last_name
        current_client.type_document = client.type_document
        current_client.num_document = client.num_document
        current_client.document_from = client.document_from
        current_client.expedition_date_document = client.expedition_date_document
        current_client.birth_date = client.birth_date
        current_client.birth_city = client.birth_city
        current_client.sex = client.sex
        current_client.telephone_number_1 = client.telephone_number_1
        current_client.telephone_number_2 = client.telephone_number_2
        current_client.email = client.email
        current_client.city_residence = client.city_residence
        current_client.civil_status = client.civil_status
        current_client.address_1 = client.address_1
        current_client.address_2 = client.address_2
        current_client.profession = client.profession
        current_client.fixed_income_value = client.fixed_income_value
        current_client.other_income = client.other_income
        current_client.approved_credit = client.approved_credit
        current_client.status_credit = client.status_credit
        current_client.maximum_amount = client.maximum_amount
        current_client.minimum_amount = client.minimum_amount
        current_client.risk_level = client.risk_level
        current_client.habit_pay = client.habit_pay
        current_client.debt_value = client.debt_value
        current_client.fixed_expenses = client.fixed_expenses
        current_client.data_credit_point = client.data_credit_point
        current_client.account_bank = client.account_bank
        current_client.type_account_bank = client.type_account_bank
        current_client.observation = client.observation
        current_client.status = client.status
        self.db.commit()

        return {
            "status": True,
            "message": "Cliente actualizado de forma correcta"
        }
    

    def update_reference(self, id, reference: ReferencesClientModel):
        
        current_reference = self.get_reference(id=id)

        current_reference.frist_name = reference.frist_name
        current_reference.last_name = reference.last_name
        current_reference.telephone_number = reference.telephone_number
        current_reference.type_reference = reference.type_reference
        current_reference.relation = reference.relation
        current_reference.update_date = datetime.now()
        current_reference.status = reference.status
        self.db.commit()
        
        return {
            "status": True,
            "message": "Referencia actualizada de forma correcta"
        }


    def update_propertie(self, id, propertie: PropertieClientModel):
        
        current_propertie = self.get_propertie(id=id)

        current_propertie.name = propertie.name
        current_propertie.description = propertie.description
        current_propertie.value = propertie.value
        current_propertie.status_range = propertie.status_range
        current_propertie.status = propertie.status
        current_propertie.type_properties_id = propertie.type_properties_id
        self.db.commit()
        
        return {
            "status": True,
            "message": "Propiedad actualizada de forma correcta"
        }
    

    def delete_reference(self, id):

        self.db.query(ReferencesClientModel).filter(ReferencesClientModel.id == id).delete()
        self.db.commit()
        
        return {
            "status": True,
            "message": "Referencia Eliminada de forma correcta"
        }
    
    
    def delete_propertie(self, id):

        self.db.query(PropertieClientModel).filter(PropertieClientModel.id == id).delete()
        self.db.commit()
        
        return {
            "status": True,
            "message": "Propiedad eliminada de forma correcta"
        }


        

        


        
    