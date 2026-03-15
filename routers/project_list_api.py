from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api/project-list")

@router.get("/")
async def get_all_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Sadece listeleme için gereken veriyi çekiyoruz
        query = "SELECT * FROM projects ORDER BY id DESC"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
