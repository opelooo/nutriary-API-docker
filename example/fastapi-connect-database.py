import mysql.connector
from slowapi import Limiter
from mysql.connector import Error
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

def get_db_connection():
    connection = mysql.connector.connect(
        host="<example_ip>",          # Use your MariaDB host (public or private IP)
        user="<example_user>",       # Replace with your MariaDB username
        password="<example_password>", # Replace with your MariaDB password
        database="<example_db>"        
    )
    return connection

@app.get("/get-data")
@limiter.limit("100/minute")  # Limit to as many as you want requests per minute per IP
def read_employees(request: Request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to return rows as dict
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"employees": rows}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
