import os
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

def get_db_connection():
    # Render panelinde "Key" kısmına ne yazdıysan onu buraya yazmalısın
    db_pass = os.getenv("DB_PASSWORD") 
    
    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=db_pass, # Burası artık yukarıdaki değişkenden şifreyi alacak
        database="aykor_dev", # Burayı 'aykor_dev' (alt tire) olarak da kontrol et gerekirse
        ssl_ca="skysql_ca.pem", 
        ssl_verify_cert=True
    )

@app.get("/test-db")
def test_connection():
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            # 'buffered=True' kullanarak sonuçların hafızada tutulmasını sağlıyoruz
            cursor = conn.cursor(buffered=True) 
            cursor.execute("SELECT 1")
            cursor.fetchone() # Gelen cevabı oku (Unread result hatasını önler)
            cursor.close()
            conn.close()
            return {
                "status": "BAŞARILI", 
                "mesaj": "Tebrikler! MariaDB Cloud ile bağlantı resmen sağlandı.",
                "detay": "ERP projenin veritabanı motoru artık çalışıyor."
            }
        return {"status": "BAĞLANTI YOK", "detay": "Bağlantı kuruldu ama aktif değil."}
    except Exception as e:
        return {"status": "HATA", "detay": str(e)}

@app.get("/")
def read_root():
    return {"status": "Uygulama çalışıyor", "test_url": "/test-db"}
