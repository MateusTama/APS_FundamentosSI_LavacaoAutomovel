import psycopg2
from config import DATABASE

def get_connection():
    conn = psycopg2.connect(database=DATABASE["database"], 
                            user=DATABASE["user"],
                            password=DATABASE["password"],
                            host=DATABASE["host"],
                            port=DATABASE["port"])
    return conn

