from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api")

# Veri Modeli - Diğer modüllerle uyumlu hale getirildi
class ProjectCreate(BaseModel):
    project_code: str
    priority: Optional[int] = None
    customer: str
    customer_group: Optional[str] = None
    subject: str
    item_quantity: int
    deadline: Optional[str] = None
    deadline_time: Optional[str] = "10:00"
    proengineer: Optional[str] = "Atanmadı"
    prostatus: str
    annodate: Optional[str] = None
    tender_reference: Optional[str] = None

# 1. TÜM PROJELERİ LİSTELE (Kritik: id eklendi)
@router.get("/projects")
async def list_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Sütun listesine 'id' eklendi, böylece frontend projeyi tanıyabilir
        query = """SELECT id, project_code, priority, customer, customer_group, subject, item_quantity, 
                          deadline, deadline_time, proengineer, prostatus, annodate, 
                          tender_reference FROM projects ORDER BY id DESC"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. YENİ PROJE EKLE
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

# 3. TEK BİR PROJEYİ GETİR (Edit Sayfası İçin)
@router.get("/get/{item_id}")
async def get_project(item_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        if not item:
            raise HTTPException(status_code=404, detail="Proje bulunamadı")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. MEVCUT PROJEYİ GÜNCELLE
@router.post("/update/{item_id}")
async def update_project(item_id: int, project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # SQL sorgusu tüm alanları kapsayacak şekilde genişletildi
        sql = """UPDATE projects SET 
                 project_code=%s, priority=%s, customer=%s, customer_group=%s, 
                 subject=%s, item_quantity=%s, deadline=%s, deadline_time=%s, 
                 proengineer=%s, prostatus=%s, annodate=%s, tender_reference=%s 
                 WHERE id=%s"""
        values = (project.project_code, project.priority, project.customer, project.customer_group,
                  project.subject, project.item_quantity, project.deadline, project.deadline_time,
                  project.proengineer, project.prostatus, project.annodate, project.tender_reference,
                  item_id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
