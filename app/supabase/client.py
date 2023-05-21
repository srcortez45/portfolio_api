from supabase import create_client, Client
from app.models.user import ClientHost
from app.models.credentials import Session
from app.models.supabase import APIResponse
from app.utils.settings import cnf
import json

class ClientManager():


    def __init__(self):
        self.supabase: Client = create_client(cnf.DB_CLOUD_CONFIG.supabase_url,
                                              cnf.DB_CLOUD_CONFIG.supabase_key)


    def get_client(self) -> Client:
        return self.supabase
    

    def save_temp_auth(self, client_host:ClientHost):
        data:APIResponse = self.get_client()\
                .table('host_client')\
                .insert(json.loads(client_host.json()))\
                .execute()
            
        return data.data
    

    def save_session(self,session:Session):
        data = self.get_client() \
                   .table("session") \
                   .insert(json.loads(session.json())) \
                   .execute()
        return data


    def get_temp_auth(self, id:str) -> ClientHost:
            data = self.get_client()\
                .table('host_client')\
                .select('*')\
                .eq('id', id)\
                .execute()
            return ClientHost(**data.data[0]) if data.data else ClientHost()
    

    def delete_temp_auth(self, id:str):
         data = self.get_client() \
         .table('host_client') \
         .delete() \
         .eq('id', id) \
         .execute()
         return data


    def get_session(self, id:str) -> Session:
        data = self.get_client() \
                   .table("session") \
                   .select("*") \
                   .eq("id", id) \
                   .limit(1) \
                   .execute()
        return Session(**data.data[0]) if len(data.data) > 0 else Session()
