from app.utils.settings import cnf
from app.models.credentials import Session, Client_Secret
from app.models.user import ClientHost
from app.models.request import SessionRequest
from app.models.response import GenerateURLResponse, SessionResponse
from app.supabase.client import ClientManager

from pydantic.tools import parse_file_as
from pydantic import HttpUrl

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build,Resource
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from  google.auth.exceptions import RefreshError

import os
import datetime

class ServiceManager():


    def __init__(self):
        self.CLIENT_FILE = cnf.BASE_PATH +'/app/resources/token.json'
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
        return build(serviceName=service_name,
                     version=api_version,
                     credentials=credentials)  
     

    def generate_url(self, client_host:ClientHost) -> HttpUrl:
        has_active_session = self.validate_session(client_host.id)
        if has_active_session:
            return GenerateURLResponse(active_session = has_active_session).dict()
        client_file = self.get_client_credentials()      
        flow = Flow.from_client_config(client_file.dict(), self.SCOPES)
        flow.redirect_uri = f'{client_host.base_url}generate-session'
        auth_url, _ = flow.authorization_url(access_type='offline',
                                             include_granted_scopes='true')
        host_client_db = ClientManager().get_temp_auth(client_host.id)
        if host_client_db.id != client_host.id:
            ClientManager().save_temp_auth(client_host)
        return GenerateURLResponse(url = auth_url,
                                   active_session = has_active_session).dict()
  

    def session_flow(self, id:str , url:str):
        session_request = SessionRequest(id=id, url_response=url)
        has_active_session = self.validate_session(session_request.id)
        if has_active_session:
            return SessionResponse(session_type='session', message='active_session')
        has_temp_auth = self.validate_temp_auth(session_request.id)
        if has_temp_auth:
            self.generate_new_session(id=session_request.id,url=session_request.url_response)
            return SessionResponse(session_type='temp', message='new_session')
    

    def generate_new_session(self, id:str, url:str):
        client_host:ClientHost = ClientManager().get_temp_auth(id)
        client_file = self.get_client_credentials()
        flow = Flow.from_client_config(client_file.dict(), self.SCOPES)
        flow.redirect_uri = f'{client_host.base_url}generate-session'
        authorization_response = url
        try:
            flow.fetch_token(authorization_response=authorization_response)
        except Exception as e:
            print('error fetching token')
            print(str(e))
            return   
        credentials = flow.credentials
        session_credentials = Session.parse_raw(credentials.to_json())
        session_credentials.expiry = credentials.expiry.strftime('%Y-%m-%d %H:%M:%S')
        session_credentials.id = id
        ClientManager().save_session(session_credentials)  


    def get_last_session(self, id:str) -> Credentials:
        session_credentials:Session = ClientManager().get_session(id)
        credentials = Credentials(
                token=session_credentials.token,
                refresh_token=None,
                id_token=session_credentials.id_token,
                token_uri=session_credentials.token_uri,
                client_id=session_credentials.client_id,
                client_secret=session_credentials.client_secret,
                scopes=session_credentials.scopes,
        )     
        expiry = session_credentials.expiry
        expiry_datetime = datetime.datetime.strptime(expiry,'%Y-%m-%d %H:%M:%S')
        credentials.expiry = expiry_datetime
        return credentials
        

    def refresh_credentials(self, credentials:Credentials) -> Credentials:
        try:
            if credentials.valid or credentials.expired:
                print('refresh credencials')
                request = Request()
                credentials.refresh(request)
            print('not refresh credentials')      
            return credentials
        except RefreshError:
            print('an error occurred while refreshing credentials')
            return credentials  


    def validate_session(self, id:str) -> bool:
        session:Session = ClientManager().get_session(id)
        return True if session.id == id else False
    
    def validate_temp_auth(self, id:str) -> bool:
        client_host:ClientHost = ClientManager().get_temp_auth(id)
        return True if client_host.id == id else False       
    

    def get_client_credentials(self) -> Client_Secret:
        try:
            return parse_file_as(path=self.CLIENT_FILE, type_=Client_Secret)
        except Exception as e:
            print('an error occurred while reading the client credentials')
            print(str(e))
            raise Exception