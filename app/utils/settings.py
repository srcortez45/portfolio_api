from pydantic import BaseModel,BaseSettings, Field
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class DBCloudConfig(BaseSettings):
    supabase_url:str = Field(env="url_supabase")
    supabase_key:str = Field(env="key_supabase")
    api_key: str = Field(env="api_key")
    db: str = Field(env="db")
    api_config: str = Field(env="api_config")
    api_token_config: str = Field(env="api_token_config")
    secret_id: str = Field(env="aws_id")
    access_key: str = Field(env="aws_key")
    region: str = Field(env="aws_region")
    
    class Config:
        env_file_encoding = 'utf-8'

class NotificationConfig(BaseSettings):
    channel:str = Field(env="bot_channel")
    token:str = Field(env="bot_token")
    
    class Config:
        env_file_encoding = 'utf-8'


class AppConfig(BaseModel):
    DESCRIPTION: str = 'API to fetch data from portfolio projects'
    VERSION: float = 1.0
    PORT: int = 8000
    tags_metadata = [
        {
            "name":"google auth",
            "description":"login from google"
        },
        {
            "name":"user cv",
            "description":"get the user information"
        }
    ]

class GlobalConfig(BaseSettings):

    BASE_PATH:str = os.getcwd()

    LOG_LEVEL:str = Field(env="DEFAULT_LOG_LEVEL")

    REDIS: str = Field(env="REDIS")
    #OAUTHLIB_TRANSPORT: str = Field(env="OAUTHLIB_TRANSPORT")

    APP_CONFIG: AppConfig = AppConfig()

    DB_CLOUD_CONFIG: DBCloudConfig = DBCloudConfig(_env_file='.env', 
                                                   _env_file_encoding='utf-8')

    NOTIFICATION_CONFIG: NotificationConfig = NotificationConfig(
                                                   _env_file='.env', 
                                                   _env_file_encoding='utf-8')

    ENV_STATE: Optional[str] = Field(None,env="ENV_STATE")
    class Config:

        env_file: str = ".env"
        
class DevConfig(GlobalConfig):
    """Development configurations."""

    TITLE: str = 'PORTFOLIO API - DEV'

    DEBUG:bool = True

    openapi_url:Optional[str] = '/api/openapi'

    docs_url:Optional[str] = '/docs'
    
    redoc_url:Optional[str] = '/redoc'

    proxy_headers: bool = False

        
class ProdConfig(GlobalConfig):
    """Production configurations."""

    TITLE: str = 'PORTFOLIO API - PROD'

    DEBUG:bool = False

    openapi_url:Optional[str] = '/api/openapi'

    docs_url:Optional[str] = '/api/documentation'
    
    redoc_url:Optional[str] = None

    proxy_headers: bool = True
        
class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()

cnf = FactoryConfig(GlobalConfig().ENV_STATE)()