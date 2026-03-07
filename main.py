import os
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=os.getenv("DB_PASSWORD"),
        database="defaultdb", # Panelde gördüğün kesin isimle değiştir
        ssl_ca="skysql_ca.pem",
        ssl_verify_cert=True
    )

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    # Ana sayfayı (dashboard.html) yükler
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/projects")
def get_projects_api():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # Verileri sözlük yapısında (JSON gibi) getirir
        cursor.execute("SELECT project_code, customer, subject, prostatus FROM projects LIMIT 50")
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        return projects
    except Exception as e:
        return {"error": str(e)}
