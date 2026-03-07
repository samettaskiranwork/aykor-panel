import os
import mysql.connector
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

def get_test_connection():
    # Render'daki 'Environment Variables' kısmına eklediğin şifreyi kullanır
    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=os.getenv("DB_PASSWORD"), 
        database="asıl_veritabanı_adın", # Burayı SkySQL'deki DB adınla değiştir!
        ssl_ca="skysql_ca.pem", # Sertifika dosyan GitHub'da olmalı
        ssl_verify_cert=True
    )

@app.get("/test-db")
def test_db():
    try:
        conn = get_test_connection()
        cursor = conn.cursor()
        # Tablodaki toplam satır sayısını soralım
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {
            "status": "BAŞARILI!",
            "mesaj": f"MariaDB Cloud'a bağlandım. Tabloda {count} adet proje buldum.",
            "database_host": "SkySQL Serverless"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "HATA", "detay": str(e)}
        )

@app.get("/")
def home():
    return {"mesaj": "API Çalışıyor. Test için /test-db adresine git."}
