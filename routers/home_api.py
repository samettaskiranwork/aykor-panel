from fastapi import APIRouter, HTTPException # APIRouter'ı buraya ekledik
from database import get_db_connection
from datetime import datetime, timedelta

# BU SATIR EKSİK VEYA AŞAĞIDA KALMIŞ:
router = APIRouter(prefix="/api/home")

@router.get("/dashboard_data")
async def get_dashboard_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # --- TARİH AYARLARI ---
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        
        # SQL'e göndermeden önce metne çevirmek her zaman daha güvenlidir
        today_str = today.strftime('%Y-%m-%d')
        next_week_str = next_week.strftime('%Y-%m-%d')

        # --- KRİTİK PROJELER SORGUSU ---
        # 1. CAST ile statüyü metne çeviriyoruz (Integer ise hata almamak için)
        # 2. BETWEEN yerine <= kullanarak 'Gecikmiş' ama hala aktif işleri de dahil ediyoruz
        query = """
            SELECT project_code, customer, subject, deadline, prostatus 
            FROM projects 
            WHERE CAST(prostatus AS CHAR) LIKE '10%' 
            AND deadline <= %s
            AND deadline >= '2000-01-01'
            ORDER BY deadline ASC
        """
        # Test amaçlı: Sadece önümüzdeki 7 günü değil, 
        # statüsü 10 olup süresi dolmuş TÜM işleri getiriyoruz (Gerçekten kritikler bunlardır)
        cursor.execute(query, (next_week_str,))
        upcoming = cursor.fetchall()

        # --- LOGLAMA (Terminalden kontrol etmen için) ---
        print(f"Sorgu Tarihi: {next_week_str} tarihine kadar olanlar aranıyor.")
        print(f"Bulunan Kayıt Sayısı: {len(upcoming)}")

        # ... (İstatistik kısımları aynı kalabilir) ...
        
        cursor.execute("SELECT COUNT(*) as count FROM projects WHERE prostatus LIKE '10%'")
        working_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM budget")
        budget_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM future")
        future_count = cursor.fetchone()['count']

        cursor.close()
        conn.close()

        return {
            "stats": {"working": working_count, "budget": budget_count, "future": future_count},
            "upcoming_projects": upcoming
        }
    except Exception as e:
        print(f"HATA OLUŞTU: {str(e)}") # Terminale hatayı yazdır
        raise HTTPException(status_code=500, detail=str(e))
