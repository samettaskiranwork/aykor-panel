from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api/future")

# Veri Modeli (NULL değerlere izin vermek için Optional yaptık)
class ProjectCreate(BaseModel):
    project_code: str
    priority: Optional[int] = None
    customer: str
    customer_group: Optional[str] = None
    subject: str
    item_quantity: int
    deadline: Optional[str] = None
    deadline_time: Optional[str] = "10:00"
    prostatus: str
    annodate: Optional[str] = None
    tender_reference: Optional[str] = None

# 1. LİSTELEME
@router.get("/list")
async def list_future_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM future_projects ORDER BY id DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. EKLEME
@router.post("/add")
async def create_future_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO future_projects 
                 (project_code, priority, customer, customer_group, subject, item_quantity, deadline, prostatus, annodate, tender_reference) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (project.project_code, project.priority, project.customer, project.customer_group, 
                  project.subject, project.item_quantity, project.deadline, project.prostatus, 
                  project.annodate, project.tender_reference)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. TEK BİR PROJE GETİRME (YENİ - Düzenleme ekranı için)
@router.get("/get/{item_id}")
async def get_future_project(item_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM future_projects WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        if not item:
            raise HTTPException(status_code=404, detail="Future projesi bulunamadı")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. GÜNCELLEME (YENİ!)
@router.post("/update/{item_id}")
async def update_future_project(item_id: int, project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE future_projects SET 
                 project_code=%s, priority=%s, customer=%s, subject=%s, 
                 item_quantity=%s, deadline=%s, prostatus=%s 
                 WHERE id=%s"""
        values = (project.project_code, project.priority, project.customer, project.subject, 
                  project.item_quantity, project.deadline, project.prostatus, item_id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
