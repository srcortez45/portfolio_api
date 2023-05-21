from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class Session(BaseModel):
    id: Optional[UUID4] = 'no_id'
    state: Optional[str] = 'no_state'
    token: Optional[str] = 'no_token'
    refresh_token: Optional[str] = 'no_ref_token'
    id_token: Optional[str] = 'no_id_token'
    token_uri: Optional[str] = 'no_uri_token'
    client_id: Optional[str] = 'no_client_id'
    client_secret: Optional[str] = 'no_client_secret'
    scopes: Optional[List[str]] = 'no_scopes'
    expiry: Optional[str] = datetime.now()

class Client_OAuth2(BaseModel):
    client_id: str
    project_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_secret: str
    redirect_uris: List[str]
    javascript_origins: List[str]    

class Client_Secret(BaseModel):
    web: Client_OAuth2