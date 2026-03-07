import os
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Veritabanı bağlantı ayarları
def get_db_connection():
    try:
        # Render Secret File olarak eklediğin dosya yolu varsayılan olarak ana dizindedir
        return mysql.connector.connect(
            host="serverless-eu-central-1.sysp0000.db1.skysql.com",
            port=4042,
            user="dbpwf34135244",
            password=os.getenv("FvETeQKGI8(FNcYKhlP0fat"), 
            database="aykor_dev", # Buraya kendi oluşturduğun DB ismini yazmayı unutma!
            ssl_ca="skysql_ca.pem", 
            ssl_verify_cert=True
        )
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None

@app.get("/test-db")
def test_connection():
    conn = get_db_connection()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM projects")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {
            "status": "BAŞARILI",
            "message": f"MariaDB Cloud'a bağlandım. Tabloda toplam {total} satır var.",
            "source": "SkySQL Serverless"
        }
    else:
        return JSONResponse(
            status_code=500,
            content={"status": "HATA", "message": "Veritabanına bağlanılamadı. Şifre veya IP iznini kontrol et."}
        )

@app.get("/")
def read_root():
    return {"status": "Uygulama çalışıyor", "test_url": "/test-db"}
