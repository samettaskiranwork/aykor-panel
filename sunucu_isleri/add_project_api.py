from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/api/add-project")


class ProjectCreate(BaseModel):
    project_code: str
    priority: int
    customer_groups: str
    customer: str
    subject: str
    item_quantity: int
    deadline: Optional[str] = None
    proengineer: str
    project_type: str


@router.get("/dropdowns")
async def get_dropdowns():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT group_name FROM customer_groups")
        groups = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT customer_name FROM customers")
        customers = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT full_name FROM users")
        engineers = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {"groups": groups, "customers": customers, "engineers": engineers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO projects (project_code, priority, customer_group, customer, subject, 
                 item_quantity, deadline, proengineer, project_type, prostatus) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, '10')"""
        values = (
            project.project_code,
            project.priority,
            project.customer_groups,
            project.customer,
            project.subject,
            project.item_quantity,
            project.deadline,
            project.proengineer,
            project.project_type,
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
