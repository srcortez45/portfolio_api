from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class Session(BaseModel):
    state: str
    token: str
    refresh_token: str
    id_token: Optional[str]
    token_uri: HttpUrl
    client_id: str
    client_secret: str
    scopes: List[str]
    expiry: str

class Client_OAuth2(BaseModel):
    client_id: str
    project_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_secret: str
    redirect_uris: List[str]    

class Client_Secret(BaseModel):
    installed: Client_OAuth2