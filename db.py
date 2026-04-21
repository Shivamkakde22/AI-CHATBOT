import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """Establish and return a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_Name"),
            user=os.getenv("DB_user"),
            password=os.getenv("DB_password"),
            host=os.getenv("DB_host"),
            port=os.getenv("DB_port")
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        return None