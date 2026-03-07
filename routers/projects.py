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
    tender_reference: Optional[str] = None
    annodate: Optional[str] = None
    prostatus: str

@router.get("/projects")
async def list_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Senin istediğin tüm detaylı sütunlar:
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
                 (project_code, priority, customer, customer_group, subject, item_quantity, deadline, tender_reference, annodate, prostatus) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (project.project_code, project.priority, project.customer, project.customer_group, 
                  project.subject, project.item_quantity, project.deadline, project.tender_reference, 
                  project.annodate, project.prostatus)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
