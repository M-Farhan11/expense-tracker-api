from mysql.connector import pooling
import os 
import dotenv
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

passw = os.getenv("DB_PASSWORD")



db_pool = pooling.MySQLConnectionPool(
   pool_name = "expense_pool",
   pool_size = 10,
    host = "localhost",
    user = "root",
    password = passw,
    database = "expense_tracker"
)

def get_db():
   try:
      return db_pool.get_connection()
   except Exception:
      raise HTTPException(
         status_code= 500,
         detail= "Database Connection Failed"
      )