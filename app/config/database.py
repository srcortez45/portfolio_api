from app.utils.settings import cnf
import boto3
class Client:
    
    def get_connection(self,table_name:str) -> boto3.resource:
        return boto3.resource(cnf.DB_CLOUD_CONFIG.db,
            aws_access_key_id=cnf.DB_CLOUD_CONFIG.secret_id,
            aws_secret_access_key=cnf.DB_CLOUD_CONFIG.access_key,
            region_name=cnf.DB_CLOUD_CONFIG.region).Table(table_name)