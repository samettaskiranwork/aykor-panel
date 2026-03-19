import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    # Render'da mıyız yoksa Samet'in bilgisayarında mı anlamak için basit bir kontrol:
    # Eğer Render'daysak 'RENDER' diye bir değişken sistemde olur.
    is_render = os.getenv("RENDER") 

    if is_render:
        # RENDER AYARI: Dosya yolu sunucuya göre (aykor-panel klasörünün içinde olmalı)
        ca_path = "globalsignrootca.pem"
    else:
        # SENİN BİLGİSAYARIN: Kendi yolun
        ca_path = r"C:\Users\Samet\Desktop\Kodlar\APY\globalsignrootca.pem"

    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=os.getenv("DB_PASSWORD"), # Hem yerelde hem Render'da çalışır!
        database="aykor_dev", 
        ssl_ca=ca_path,
        ssl_verify_cert=True
    )