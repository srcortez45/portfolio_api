from app.utils.settings import cnf
from app.utils.toolbox import timer
from app.models.credentials import Session,Client_Secret
from app.supabase.client import ClientManager

from pydantic.tools import parse_file_as
from pydantic import HttpUrl

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build,Resource
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from  google.auth.exceptions import RefreshError

import json
import os
import datetime

class ServiceManager():

    def __init__(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.CLIENT_FILE = cnf.BASE_PATH +'\\app\\resources\\token.json'
        self.SESSION_FILE = cnf.BASE_PATH +'\\app\\resources\\session.json'
        self.SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
        self.SERVICE_NAME = 'docs'
        self.API_VERSION = 'v1'

    def get_service(self) -> Resource:

        credentials = self.get_credentials(self.CLIENT_FILE,self.SCOPES)

        service = None

        if credentials is None:
            print('no hay credenciales validas')

        else:
            service = self.create_service(self.SERVICE_NAME,
                                          self.API_VERSION,
                                          credentials)
            print('service created')

        print('fin del flujo')
        return service   
                    
    def create_service(self,service_name:str,api_version:str, credentials:Credentials):
        return build(service_name, api_version, credentials)  
    
    def generate_url(self) -> HttpUrl:

        client_file = self.get_client_credentials()
                    
        flow = Flow.from_client_config(client_file.dict(), self.SCOPES)

        flow.redirect_uri = 'http://localhost:8000/generate-session'

        auth_url, _ = flow.authorization_url(access_type='offline',
                                            include_granted_scopes='true')
        return auth_url
    
    def create_session(self,url:str):

        client_file = self.get_client_credentials()

        flow = Flow.from_client_config(client_file.dict(), self.SCOPES)

        flow.redirect_uri = 'http://localhost:8000/generate-session'

        authorization_response = url

        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        session_credentials = Session.parse_raw(credentials.to_json())
                              #parse_obj_as(User, user_dict)

        session_credentials.expiry = credentials.expiry.strftime('%Y-%m-%d %H:%M:%S')

        with open(cnf.BASE_PATH +'\\app\\resources\\session.json', 'w') as f: 
            json.dump(session_credentials.dict(), f)
            f.close()

        return 'session created'
    
    def get_credentials(self) -> Credentials:
            
        session_credentials = self.get_session_credentials()

        credentials = Credentials(
                token=session_credentials.token,
                refresh_token=session_credentials.refresh_token,
                id_token=session_credentials.id_token,
                token_uri=session_credentials.token_uri,
                client_id=session_credentials.client_id,
                client_secret=session_credentials.client_secret,
                scopes=session_credentials.scopes,
        )
            
        expiry = session_credentials.expiry
        expiry_datetime = datetime.datetime.strptime(expiry,'%Y-%m-%d %H:%M:%S')
        credentials.expiry = expiry_datetime

        try:

            if credentials.valid or credentials.expired:
                request = Request()
                credentials.refresh(request)
                        
            return credentials

        except RefreshError:
            print('an error occurred while refreshing credentials')
            open(cnf.BASE_PATH +'\\app\\resources\\session.json', 'w').close()     

    @timer
    def clear_access(self):
        
        try:
            open(cnf.BASE_PATH +'\\app\\resources\\session.json', 'w').close()
            return 'clear success'
        except Exception as e:
            print('an error occurred while clearing credentials')
            print(str(e))

    def get_session_credentials(self) -> Session | None:

        try:
            response = ClientManager().get_session()
            user_session = Session(**response.data[0])
            user_session.dict()
            return parse_file_as(path=self.SESSION_FILE, type_=Session)
            
        except Exception as e:
            print('an error occurred while reading the session credentials')
            print(str(e))
            raise Exception
        
    def get_client_credentials(self) -> Client_Secret | None:

        try:
            if os.stat(self.CLIENT_FILE).st_size == 0:
                return None
            
            return parse_file_as(path=self.CLIENT_FILE, type_=Client_Secret)
            
        except Exception as e:
            print('an error occurred while reading the client credentials')
            print(str(e))
            raise Exception
