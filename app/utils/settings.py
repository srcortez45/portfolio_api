import os
from pydantic import BaseModel,BaseSettings,Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class DBCloudConfig(BaseSettings):
    supabase_url:str = Field(env="url_supabase")
    supabase_key:str = Field(env="key_supabase")
    api_key: str = Field(env="api_key")
    db: str = Field(env="db")
    secret_id: str = Field(env="aws_id")
    access_key: str = Field(env="aws_key")
    region: str = Field(env="aws_region")
    
    class Config:
        env_file_encoding = 'utf-8'

class AppConfig(BaseModel):
    DESCRIPTION: str = 'API to fetch data from portfolio projects'
    VERSION: float = 1.0
    PORT: int = 8000
    tags_metadata = [
        {
            "name":"user information",
            "description":"get the user basic information"
        },
        {
            "name":"user skills",
            "description":"get the user skills"
        }
    ]

class GlobalConfig(BaseSettings):

    BASE_PATH:str = os.getcwd()

    HOST: str = Field(env="HOST")

    #OAUTHLIB_TRANSPORT: str = Field(env="OAUTHLIB_TRANSPORT")

    APP_CONFIG: AppConfig = AppConfig()

    DB_CLOUD_CONFIG: DBCloudConfig = DBCloudConfig(_env_file='.env', _env_file_encoding='utf-8')

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