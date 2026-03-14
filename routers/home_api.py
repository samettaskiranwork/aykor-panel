from fastapi import APIRouter, HTTPException
from database import get_db_connection
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/home")

@router.get("/dashboard_data")
async def get_dashboard_data():
    """Home sayfasının ihtiyacı olan tüm veriyi tek pakette gönderir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # --- 1. İSTATİSTİK SAYILARI ---
        # Çalışan Projeler
        cursor.execute("SELECT COUNT(*) as count FROM projects WHERE prostatus LIKE '10%'")
        working_count = cursor.fetchone()['count']
        
        # Bütçe Çalışmaları
        cursor.execute("SELECT COUNT(*) as count FROM budget") # Tablo adın farklıysa düzelt
        budget_count = cursor.fetchone()['count']
        
        # Gelecek Projeler
        cursor.execute("SELECT COUNT(*) as count FROM future") # Tablo adın farklıysa düzelt
        future_count = cursor.fetchone()['count']

        # --- 2. KRİTİK PROJELER (STATUS 10 & 7 GÜN) ---
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        
        query = """
            SELECT project_code, customer, subject, deadline, prostatus 
            FROM projects 
            WHERE prostatus LIKE '10%' 
            AND deadline BETWEEN %s AND %s
            ORDER BY deadline ASC
        """
        cursor.execute(query, (today, next_week))
        upcoming = cursor.fetchall()

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
        raise HTTPException(status_code=500, detail=f"Home API Hatası: {str(e)}")
