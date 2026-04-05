from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api/firms")

class CustomerCreate(BaseModel):
    customer_name: str
    group_id: int
    representative: str
    website: Optional[str] = None

@router.get("/list")
async def list_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT c.*, g.group_name FROM customers c LEFT JOIN customer_groups g ON c.group_id = g.id")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

@router.post("/add")
async def add_customer(data: CustomerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO customers (customer_name, group_id, representative, website) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data.customer_name, data.group_id, data.representative, data.website))
    conn.commit()
    return {"status": "success"}

@router.get("/groups")
async def get_groups():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer_groups")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res
