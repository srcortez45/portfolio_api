from supabase import create_client, Client

from app.utils.settings import cnf

import uuid

class ClientManager():

    def __init__(self):
        self.supabase: Client = create_client(cnf.DB_CLOUD_CONFIG.supabase_url, cnf.DB_CLOUD_CONFIG.supabase_key)

    def get_client(self) -> Client:
        return self.supabase
    
    def save_session(self):

        print('guardo')

        data = self.get_client().table("session").insert(
            {"state":"1234",
             "token": "test",
             "refresh_token":"test",
             "id_token":"test",
             "token_uri":"test",
             "client_id":"test",
             "client_secret":"test",
             "scopes":["12345"],
             "expiry":"2023-04-01 20:00:00",
             "id":str(uuid.uuid4())
            }
            
            ).execute()

        
        print('termino')
        #print(data)
        #cred: SignInWithPasswordCredentials
        
        #user.
        #print(user)

        #user_api@supabase.com
        #1234

        return 'test'

    def get_session(self):
        data = self.get_client().table("session").select("*").eq("state","12345").execute()
        return data
