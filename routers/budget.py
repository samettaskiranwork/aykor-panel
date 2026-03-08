from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api/budget")

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

@router.get("/list")
async def list_budget_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM budget_projects ORDER BY id DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
async def create_budget_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO budget_projects 
                 (project_code, priority, customer, customer_group, subject, item_quantity, deadline, deadline_time, prostatus, annodate, tender_reference) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (project.project_code, project.priority, project.customer, project.customer_group, 
                  project.subject, project.item_quantity, project.deadline, project.deadline_time,
                  project.prostatus, project.annodate, project.tender_reference)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
