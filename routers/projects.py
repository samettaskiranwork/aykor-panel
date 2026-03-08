from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api")

class ProjectCreate(BaseModel):
    project_code: str
    priority: int
    customer: str
    customer_group: str
    subject: str
    item_quantity: int
    deadline: Optional[str] = None
    deadline_time: Optional[str] = "10:00"
    proengineer: Optional[str] = "Atanmadı"
    prostatus: str
    annodate: Optional[str] = None
    tender_reference: Optional[str] = None

@router.get("/projects")
async def list_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # SORGUMUZU TÜM SÜTUNLARI ÇEKECEK ŞEKİLDE GÜNCELLEDİK
        query = """SELECT project_code, priority, customer, subject, item_quantity, 
                          deadline, deadline_time, proengineer, prostatus, annodate, 
                          tender_reference FROM projects ORDER BY id DESC"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-project")
async def create_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO projects 
                 (project_code, priority, customer, customer_group, subject, item_quantity, 
                  deadline, deadline_time, proengineer, prostatus, annodate, tender_reference) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (project.project_code, project.priority, project.customer, project.customer_group, 
                  project.subject, project.item_quantity, project.deadline, project.deadline_time,
                  project.proengineer, project.prostatus, project.annodate, project.tender_reference)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # 1. Tek bir projeyi ID ile getir
@router.get("/get/{item_id}")
async def get_project(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")
    return item

# 2. Mevcut projeyi güncelle
@router.post("/update/{item_id}")
async def update_project(item_id: int, project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE projects SET 
                 project_code=%s, priority=%s, customer=%s, subject=%s, 
                 item_quantity=%s, deadline=%s, prostatus=%s 
                 WHERE id=%s"""
        values = (project.project_code, project.priority, project.customer, 
                  project.subject, project.item_quantity, project.deadline, 
                  project.prostatus, item_id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
