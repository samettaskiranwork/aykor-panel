import os
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Veritabanı Bağlantısı
def get_db_connection():
    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=os.getenv("DB_PASSWORD"),
        database="aykor_dev", 
        ssl_ca="skysql_ca.pem",
        ssl_verify_cert=True
    )

# Yeni Proje Modeli (DDL yapısına tam uyumlu)
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

# ANA SAYFA
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# PROJE LİSTESİ ÇEKME
@app.get("/api/projects")
async def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # İstediğin tüm sütunları çekiyoruz
        query = """SELECT project_code, priority, customer, subject, item_quantity, 
                          deadline, deadline_time, proengineer, prostatus, annodate, 
                          tender_reference FROM projects ORDER BY id DESC"""
        cursor.execute(query)
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        return projects
    except Exception as e:
        return {"error": str(e)}

# PROJE EKLEME
@app.post("/api/add-project")
async def add_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO projects 
                 (project_code, priority, customer, customer_group, subject, item_quantity, 
                  deadline, deadline_time, proengineer, prostatus, annodate, tender_reference) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            project.project_code, project.priority, project.customer, project.customer_group,
            project.subject, project.item_quantity, project.deadline, project.deadline_time,
            project.proengineer, project.prostatus, project.annodate, project.tender_reference
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
