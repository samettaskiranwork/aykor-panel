import os
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

# 1. Uygulama Başlatma (Hatanın çözümü burası)
app = FastAPI()

# 2. Şablon (HTML) Klasörü Tanımlama
templates = Jinja2Templates(directory="templates")

# 3. Veritabanı Bağlantı Fonksiyonu
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

# 4. Veri Modeli (Paylaştığın DDL yapısına tam uyumlu)
class ProjectCreate(BaseModel):
    project_code: str
    priority: Optional[int] = 2
    customer: str
    customer_group: Optional[str] = None
    subject: str
    item_quantity: Optional[int] = 1
    deadline: Optional[str] = None
    deadline_time: Optional[str] = None
    proengineer: Optional[str] = None
    prostatus: Optional[str] = "Aktif"
    annodate: Optional[str] = None
    tender_reference: Optional[str] = None
    bid_bond: Optional[float] = 0.0

# ---------------------------------------------------------
# ROUTERLAR (YOLLAR)
# ---------------------------------------------------------

# ANA SAYFA: Dashboard'u yükler
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# LİSTELEME API: Projeleri veritabanından çeker
@app.get("/api/projects")
async def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # En yeni projeyi en üstte görmek için 'id DESC' ekledik
        cursor.execute("SELECT project_code, customer, subject, prostatus FROM projects ORDER BY id DESC")
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        return projects
    except Exception as e:
        return {"error": str(e)}

# EKLEME API: Formdan gelen veriyi veritabanına kaydeder
@app.post("/api/add-project")
async def add_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sütun isimleri DDL'indeki 'annodate', 'proengineer' vb. ile eşleşti
        sql = """INSERT INTO projects 
                 (project_code, priority, customer, customer_group, subject, item_quantity, 
                  deadline, deadline_time, proengineer, prostatus, annodate, 
                  tender_reference, bid_bond) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            project.project_code, project.priority, project.customer, project.customer_group,
            project.subject, project.item_quantity, project.deadline, project.deadline_time,
            project.proengineer, project.prostatus, project.annodate,
            project.tender_reference, project.bid_bond
        )
        
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": "Proje başarıyla kaydedildi."}
    except Exception as e:
        # Hata durumunda 400 koduyla hata mesajını döndür
        return {"status": "error", "message": str(e)}

# TEST YOLU: Bağlantıyı kontrol etmek için
@app.get("/test-db")
async def test_connection():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return {"status": "BAŞARILI"}
    except Exception as e:
        return {"status": "HATA", "detay": str(e)}
