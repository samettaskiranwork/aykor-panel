import mysql.connector
import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()


def get_db_connection():
    # RENDER değişkeni sadece Render.com sunucularında otomatik olarak bulunur.
    # Senin bilgisayarında bu değişken olmadığı için kod direkt 'else' (Yerel) kısmına gidecek.
    is_render = os.getenv("RENDER")

    if is_render:
        # --- BULUT (RENDER / SKYSQL) AYARLARI ---
        # Bu kısım sadece site canlıdayken çalışacak.
        print(">>> Bağlantı Durumu: SKYSQL (Bulut)")
        return mysql.connector.connect(
            host="serverless-eu-central-1.sysp0000.db1.skysql.com",
            port=4042,
            user="dbpwf34135244",
            password=os.getenv("DB_PASSWORD"),
            database="aykor_dev",
            ssl_ca=cert_path,  # Artık tam adres gidiyor
            ssl_verify_cert=True,
            connect_timeout=15,
        )
    else:
        # --- YEREL (SAMET'İN BİLGİSAYARI / LOCALHOST) AYARLARI ---
        # Bu kısım sen VS Code'da çalışırken devreye girecek.
        print(">>> Bağlantı Durumu: LOCALHOST (Yerel)")
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password=os.getenv("LOCAL_DB_PASSWORD"),  # .env içindeki Aykor2026!
            database="aykor_local",
            # Yerelde SSL sertifikasına gerek yok, o yüzden o satırları sildik.
        )
