# Expense Tracker API

A REST API for tracking personal expenses built with FastAPI and MySQL.

## Features
- Add expenses with name, amount, description, and date
- View all expenses
- Delete expenses
- Update expense amounts
- Calculate total expenses

## Tech Stack
- Python 3.x
- FastAPI
- MySQL
- Pydantic (validation)

## Setup
1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Create MySQL database named `expense_tracker`

3. Create the expenses table:
```sql
   CREATE TABLE expenses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(15) NOT NULL,
       amount DECIMAL(10,2) NOT NULL,
       description VARCHAR(100),
       expense_date DATE NOT NULL
   );
```

4. Create a `.env` file in the project root:
```
   DB_Password=your_password_here
```

5. Run the application:
```bash
   uvicorn main:app --reload
```

6. Access the API at `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/expenses` | Add new expense |
| GET | `/expenses` | View all expenses |
| DELETE | `/expenses/{id}` | Delete expense by ID |
| PUT | `/expenses/{id}` | Update expense amount |
| GET | `/expenses/total` | Get total of all expenses |

## Example Request
```json
POST /expenses
{
  "name": "Groceries",
  "amount": 150.50,
  "description": "Weekly shopping",
  "expense_date": "2025-01-27"
}
```

## Future Improvements
- Add user authentication
- Add expense categories
- Filter by date range
- Deploy to cloud (Railway/Render)
- Add pagination for expense list