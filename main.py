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
@app.get("/test-db")
def test_connection():
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            return {"status": "BAŞARILI"}
        return {"status": "BAĞLANTI YOK"}
    except Exception as e:
        # Bu satır bize gerçek hatayı söyleyecek
        return {"status": "HATA", "detay": str(e)}

@app.get("/")
def read_root():
    return {"status": "Uygulama çalışıyor", "test_url": "/test-db"}
