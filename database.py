import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    # Dosyanın adını belirleyelim
    cert_name = "globalsignrootca.pem"
    
    # Eğer senin bilgisayarındaki o özel yol varsa onu kullan, yoksa (Render'daysa) direkt dosya adını kullan
    local_path = r"C:\Users\Samet\Desktop\Kodlar\APY\aykor-panel\globalsignrootca.pem"
    
    if os.path.exists(local_path):
        ca_path = local_path
    else:
        # Render'da dosya ana dizinde olacağı için sadece ismini veriyoruz
        ca_path = cert_name

    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=os.getenv("DB_PASSWORD"),
        database="aykor_dev", 
        ssl_ca=ca_path,
        ssl_verify_cert=True,
        # Bağlantı zaman aşımını biraz artıralım ki Render rahat bağlansın
        connect_timeout=10 
    )