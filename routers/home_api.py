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

        # --- 2. İSTATİSTİK SAYILARI (GÜNCEL TABLOLAR) ---
        # Aktif Projeler (Statü 10.x olanlar)
        cursor.execute("SELECT COUNT(*) as count FROM projects WHERE CAST(prostatus AS CHAR) LIKE '10%'")
        working_count = cursor.fetchone()['count']
        
        # Bütçe Projeleri (Tablo adını düzelttik)
        cursor.execute("SELECT COUNT(*) as count FROM budget_projects")
        budget_count = cursor.fetchone()['count']
        
        # Gelecek Projeler (Tablo adını düzelttik)
        cursor.execute("SELECT COUNT(*) as count FROM future_projects")
        future_count = cursor.fetchone()['count']

        # --- 3. KRİTİK PROJELER SORGUSU ---
        # Statüsü 10.x olan ve teslim tarihi 7 gün içinde olanlar
        query = """
    SELECT 
        project_code, customer, subject, tender_reference, 
        item_quantity, deadline, deadline_time, proengineer, 
        annodate, prostatus, priority
    FROM projects 
    WHERE prostatus LIKE '10%' 
    AND deadline <= %s
    ORDER BY deadline ASC
"""
        cursor.execute(query, (next_week_str,))
        upcoming = cursor.fetchall()

        # Terminal Raporu (Hata ayıklama için)
        print(f"--- Dashboard Raporu ---")
        print(f"Aktif: {working_count}, Bütçe: {budget_count}, Gelecek: {future_count}")
        print(f"Kritik Liste: {len(upcoming)} adet bulundu.")

        cursor.close()
        conn.close()

        return {
            "stats": {
                "working": working_count,
                "budget": budget_count,
                "future": future_count
            },
            "upcoming_projects": upcoming
        }
    except Exception as e:
        print(f"!!! HOME API HATASI: {str(e)}") # Hatanın ne olduğunu terminalde gör
        raise HTTPException(status_code=500, detail=str(e))
