from fastapi import FastAPI
import mysql.connector
from mysql.connector import pooling
from pydantic import BaseModel , Field
from pydantic import validator
from datetime import date
import os 
from dotenv import load_dotenv


load_dotenv()
passw = os.getenv("DB_Password")

if passw is None:
   print("No password found! ")

db_pool = pooling.MySQLConnectionPool(
   pool_name = "expense_pool",
   pool_size = 10,
    host = "localhost",
    user = "root",
    password = passw,
    database = "expense_tracker"
)
#cursor = db.cursor(dictionary = True)
def get_db():
   return db_pool.get_connection()

app = FastAPI()
@app.get("/")
def home():
    return{"Message ": "Works "}

class Expense (BaseModel):
    name : str = Field(min_length=1 , max_length= 15)
    amount : float = Field(gt = 0 , description="Amount should be greater than 0" )
    description : str = Field(min_length= 1 , max_length= 100)
    expense_date: date
    
    @validator("expense_date")
    def validate_date(cls , v):
       if v> date.today():
          raise ValueError ("Date cannot be from future! ")
       return  v
   
   
@app.post("/expenses")
def add_expense(expense: Expense):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """INSERT INTO expenses 
             (name, amount, description, expense_date)
             VALUES (%s, %s, %s, %s)"""

    values = (
        expense.name,
        expense.amount,
        expense.description,
        expense.expense_date
    )

    try:
        cursor.execute(sql, values)
        conn.commit()
        return {"message": "Expense added successfully"}
    finally:
        cursor.close()
        conn.close()
     
       
@app.get("/expenses")
def view_expense():
   conn = get_db()
   cursor = conn.cursor(Dictoinary = True)

   cursor.execute("SELECT * FROM expenses ")
   result = cursor.fetchall()
   cursor.close()
   conn.close()
   return result


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id : int):
   conn = get_db()
   cursor = conn.cursor(Dictionary = True)

   cursor.execute("DELETE From expenses WHERE id = %s ", (expense_id, ))
   conn.commit()
   affected = cursor.rowcount
   cursor.close()
   conn.close()

   return {"message": "Deleted"} if affected else {"error": "Not found"}
   

   


@app.put("/expenses/{expense_id}")
def update_expense(expense_id : int , amount : float ):
   conn = get_db()
   cursor = conn.cursor(Dictionary = True)

   cursor.execute("UPDATE expenses SET amount = %s WHERE id = %s" , (amount , expense_id , ))
   conn.commit()
   affected = cursor.rowcount
   cursor.close()
   conn.close()

   return {"message": "Updated"} if affected else {"error": "Not found"}
    
@app.get("/expenses/total")
def calc_total():
   conn = get_db()
   cursor = conn.cursor(Dictionary = True)

   cursor.execute("SELECT sum(amount) AS total  FROM expenses ")
   result = cursor.fetchone()
   cursor.close()
   conn.close()
   return {"total": result["total"] if result["total"] else 0}   



