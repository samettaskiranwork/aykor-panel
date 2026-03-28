from fastapi import APIRouter, HTTPException
from database import get_db_connection
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/home")

@router.get("/dashboard_data")
async def get_dashboard_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # --- 1. ZAMAN AYARLARI ---
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        next_week_str = next_week.strftime('%Y-%m-%d')

        # --- 2. İSTATİSTİK SAYILARI (3 AYRI TABLO, 10 FİLTRESİ) ---
        
        # 1. Projects tablosundaki 'Çalışılanlar' (10%)
        cursor.execute("SELECT COUNT(*) as count FROM projects WHERE CAST(prostatus AS CHAR) LIKE '10%'")
        working_count = cursor.fetchone()['count']
        
        # 2. Budget Projects tablosundaki 'Bütçe İşleri' (10%)
        # NOT: Eğer bu tabloda kolon adı 'prostatus' değilse aşağıyı ona göre güncelle (örn: status)
        cursor.execute("SELECT COUNT(*) as count FROM budget_projects WHERE CAST(prostatus AS CHAR) LIKE '10%'")
        budget_count = cursor.fetchone()['count']
        
        # 3. Future Projects tablosundaki 'Gelecek İşler' (10%)
        cursor.execute("SELECT COUNT(*) as count FROM future_projects WHERE CAST(prostatus AS CHAR) LIKE '10%'")
        future_count = cursor.fetchone()['count']

        # Terminal Raporu (Buradan kontrol et, sayılar 0 geliyorsa LIKE '10%' kısmını kontrol et)
        print(f"--- SAYIM RAPORU ---")
        print(f"Working Table (10%): {working_count}")
        print(f"Budget Table (10%): {budget_count}")
        print(f"Future Table (10%): {future_count}")

        # --- 3. KRİTİK PROJELER SORGUSU (7 Günlük) ---
        # Burada da CAST kullandık ki tıklanamama sorunu bitsin
        query_upcoming = """
            SELECT 
                id, project_code, customer, subject, tender_reference, 
                item_quantity, deadline, deadline_time, proengineer, 
                annodate, prostatus, priority
            FROM projects 
            WHERE CAST(prostatus AS CHAR) LIKE '10%' 
            AND deadline <= %s
            ORDER BY deadline ASC
        """
        cursor.execute(query_upcoming, (next_week_str,))
        upcoming = cursor.fetchall()

        # --- 4. TÜM AKTİF PROJELER SORGUSU ---
        # Alt tabloyu besleyen ana liste
        query_all = """
            SELECT 
                id, project_code, customer, subject, priority,
                item_quantity, deadline, deadline_time, proengineer, prostatus,
                annodate, tender_reference
            FROM projects 
            WHERE CAST(prostatus AS CHAR) LIKE '10%'
        """
        cursor.execute(query_all)
        all_active = cursor.fetchall()

        # Terminal Logu
        print(f"--- Dashboard Raporu ---")
        print(f"Aktif: {working_count}, Kritik: {len(upcoming)}, Toplam Aktif: {len(all_active)}")

        cursor.close()
        conn.close()

        return {
            "stats": {
                "working": working_count,
                "budget": budget_count,
                "future": future_count,
            },
            "upcoming_projects": upcoming,
            "all_projects": all_active
        }
    except Exception as e:
        print(f"!!! HOME API HATASI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))