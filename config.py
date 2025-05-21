import os
from dotenv import load_dotenv

DATABASE = {}
FLASK = {} 

def configuracao_ambiente():
    if not (load_dotenv("config.env")):
        print("Não foi possível carregar as configurações de ambiente")
        return    
    
    DATABASE["database"] = os.getenv("DB_DATABASE")
    DATABASE["user"] = os.getenv("DB_USER")
    DATABASE["password"] = os.getenv("DB_PASSWORD")
    DATABASE["host"] = os.getenv("DB_HOST")
    DATABASE["port"] = os.getenv("DB_PORT")

    FLASK["secret_key"] = os.getenv("SECRET_KEY")

configuracao_ambiente()