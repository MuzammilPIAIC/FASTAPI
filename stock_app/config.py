from pydantic import BaseSettings

class Settings(BaseSettings):
    
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str


    # odoo_database_hostname: str
    # odoo_database_port: str
    # odoo_database_password: str
    # odoo_database_name: str
    # odoo_database_username: str


    class Config:
        env_file ='.env'


settings = Settings()