from app.utils.settings import cnf

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import typing
import json
import os
import datetime
import google.oauth2.credentials
import google.auth.transport.requests
import google.auth.exceptions
from googleapiclient.discovery import build,Resource

class ServiceManager():

    def __init__(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.CLIENT_FILE = cnf.BASE_PATH +'\\app\\resources\\token.json'
        self.SESSION_FILE = cnf.BASE_PATH +'\\app\\resources\\session.json'
        self.SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
        self.SERVICE_NAME = 'docs'
        self.API_VERSION = 'v1'

    def get_service(self) -> Resource:

        credentials = self.get_credentials(self.CLIENT_FILE,self.SCOPES) or None

        service = None

        if credentials is None:
            print('no hay credenciales validas')
        else:
            service = self.create_service(self.SERVICE_NAME,self.API_VERSION,credentials)
            print('service created')
        print('fin del flujo')
        return service   
                    
    def create_service(self,service_name:str,api_version:str, credentials:google.oauth2.credentials):
        return build(service_name, api_version, credentials)  
    
    def generate_url(self) -> str:

        client_file = self.get_client_credentials()
                    
        flow = Flow.from_client_config(client_file, self.SCOPES)

        flow.redirect_uri = 'http://localhost:8000/generate-session'

        auth_url, _ = flow.authorization_url(access_type='offline',
                                            include_granted_scopes='true')
        return auth_url
    
    def create_session(self,url:str):

        client_file = self.get_client_credentials()

        flow = Flow.from_client_config(client_file, self.SCOPES)

        flow.redirect_uri = 'http://localhost:8000/generate-session'

        authorization_response = url

        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        session_credentials = {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'id_token':credentials.id_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes,
                    'expiry':datetime.datetime.strftime(credentials.expiry,'%Y-%m-%d %H:%M:%S')
                }
        with open(cnf.BASE_PATH +'\\app\\resources\\session.json', 'w') as f: 
            json.dump(session_credentials, f)
            f.close()
            
        return 'session created'

    def validate_credentials(self):

        credentials = self.get_session_credentials()

        if credentials is None:
            return False         
                         
        return True    
    
    def get_credentials(self):
            
            session_credentials = self.get_session_credentials()
            
            credentials = google.oauth2.credentials.Credentials(
                token=session_credentials['token'],
                refresh_token=session_credentials['refresh_token'],
                id_token=session_credentials['id_token'],
                token_uri=session_credentials['token_uri'],
                client_id=session_credentials['client_id'],
                client_secret=session_credentials['client_secret'],
                scopes=session_credentials['scopes'],
            )
            
            expiry = session_credentials['expiry']
            expiry_datetime = datetime.datetime.strptime(expiry,'%Y-%m-%d %H:%M:%S')
            credentials.expiry = expiry_datetime

            try:

                if credentials.valid or credentials.expired:
                    request = google.auth.transport.requests.Request()
                    credentials.refresh(request)
                        
                return credentials

            except google.auth.exceptions.RefreshError as e:
                print('an error occurred while refreshing credentials')
                open(cnf.BASE_PATH +'\\app\\resources\\session.json', 'w').close()     

    def clear_access(self):
        try:
            open(cnf.BASE_PATH +'\\app\\resources\\session.json', 'w').close()
            return 'clear success'
        except Exception as e:
            print('an error occurred while clearing credentials')
            print(str(e))

    def get_session_credentials(self):
        session_credentials = None
        try:
            
            with open(self.SESSION_FILE) as session_file:
                session_credentials = json.load(session_file)
                session_file.close()

            return session_credentials
            
        except Exception as e:
            print('an error occurred while reading the session credentials')
            print(str(e))
            raise Exception
    def get_client_credentials(self):
        client_credentials = None
        try:
            
            with open(self.CLIENT_FILE) as client_temp:
                client_credentials = json.load(client_temp)
                client_temp.close()
            return client_credentials
        
        except Exception as e:
            print('an error occurred while reading the client credentials')
            print(str(e))
            raise Exception
