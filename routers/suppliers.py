from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api/suppliers")

class SupplierCreate(BaseModel):
    ncage_code: Optional[str] = None
    supplier_name: str
    country: Optional[str] = None
    website: Optional[str] = None

@router.get("/list")
async def list_suppliers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers ORDER BY supplier_name ASC")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

@router.post("/add")
async def add_supplier(data: SupplierCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO suppliers (ncage_code, supplier_name, country, website) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data.ncage_code, data.supplier_name, data.country, data.website))
    conn.commit()
    return {"status": "success"}
