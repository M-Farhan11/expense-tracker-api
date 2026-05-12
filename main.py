from fastapi import FastAPI ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel , Field
from pydantic import validator
from datetime import date
from db import get_db

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def home():
    await asyncio.sleep(2)
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
   cursor = conn.cursor(dictionary=True)

   cursor.execute("SELECT * FROM expenses ")
   result = cursor.fetchall()
   cursor.close()
   conn.close()
   return result


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id : int):
   conn = get_db()
   cursor = conn.cursor(dictionary=True)

   cursor.execute("DELETE From expenses WHERE id = %s ", (expense_id, ))
   conn.commit()
   if cursor.rowcount == 0:
      cursor.close()
      conn.close()
      raise HTTPException(
         status_code= 404,
         detail= "Expense Not Found !"
      )
   
   cursor.close()
   conn.close()

   return {"Message": "Expense deleted"} 
   

   


@app.put("/expenses/{expense_id}")
def update_expense(expense_id : int , amount : float ):
   if amount>0:
      raise HTTPException(
         status_code= 400,
         detail= " Amount cannot be less than 0"
      )
   conn = get_db()
   cursor = conn.cursor(dictionary=True)

   cursor.execute("UPDATE expenses SET amount = %s WHERE id = %s" , (amount , expense_id , ))
   conn.commit()
   if cursor.rowcount == 0:
      cursor.close()
      conn.close()
      raise HTTPException(
         status_code= 404,
         detail= "Expense Not Found !"
      )
   
   cursor.close()
   conn.close()

   return {"Message": "Expense Updated"}
    
@app.get("/expenses/total")
def calc_total():
   conn = get_db()
   cursor = conn.cursor(dictionary=True)

   cursor.execute("SELECT sum(amount) AS total  FROM expenses ")
   result = cursor.fetchone()
   cursor.close()
   conn.close()
   return {"total": result["total"] if result["total"] else 0}   

@app.get("/expenses/{expense_id}")
def get_expense(expense_id : int):
   conn = get_db()
   cursor = conn.cursor(dictionary=True)

   cursor.execute(
      "Select * From expenses WHERE id = %s",
      (expense_id,)
   )

   expense = cursor.fetchone()

   cursor.close()
   conn.close()

   if not expense:
      raise HTTPException(
         status_code= 404,
         detail= "Expense not found"
      )
   
   return expense


