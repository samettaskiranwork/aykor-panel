from fastapi import APIRouter, HTTPException
from database import get_db_connection
from typing import Dict, Any

router = APIRouter(prefix="/api/edit-projects", tags=["Edit Operations"])


# --- 1. PROJE VERİSİNİ GETİR ---
@router.get("/get/{project_id}")
async def get_project_for_edit(project_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # JOIN kullanarak iki tabloyu birleştiriyoruz
        # 'p' projects tablosu, 'ps' ise project_status tablosu için takma ad (alias)
        sql = """
            SELECT 
                p.id, 
                p.project_code, 
                p.customer, 
                p.subject, 
                p.priority, 
                p.item_quantity, 
                p.deadline, 
                TIME_FORMAT(p.deadline_time, '%H:%i') AS deadline_time, 
                p.proengineer, 
                p.prostatus, 
                p.project_type, 
                p.tender_reference, 
                p.annodate,
                ps.meaning AS status_meaning,
                ps.description AS status_description
            FROM projects p
            LEFT JOIN project_status ps ON p.prostatus = ps.status
            WHERE p.id = %s
        """
        
        cursor.execute(sql, (project_id,))
        project = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if not project:
            raise HTTPException(status_code=404, detail="Proje bulunamadı.")
            
        return project
    except Exception as e:
        # Hatanın ne olduğunu terminalde daha net görmek için:
        print(f"HATA OLUŞTU: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")


# --- 2. PROJEYİ GÜNCELLE ---
@router.post("/update/{project_id}")
async def update_existing_project(project_id: int, data: Dict[Any, Any]):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # DİKKAT: project_code SET kısmında YOK! (Değiştirilemez)
        sql = """
            UPDATE projects SET 
            priority=%s, customer_group=%s, customer=%s, subject=%s, 
            item_quantity=%s, deadline=%s, deadline_time=%s, 
            proengineer=%s, prostatus=%s, project_type=%s,
            tender_reference=%s, annodate=%s
            WHERE id=%s
        """

        values = (
            data.get("priority"),
            data.get("customer_group"),
            data.get("customer"),
            data.get("subject"),
            data.get("item_quantity"),
            data.get("deadline"),
            data.get("deadline_time"),
            data.get("proengineer"),
            data.get("prostatus"),
            data.get("project_type"),
            data.get("tender_reference"),
            data.get("annodate"),
            project_id,
        )

        cursor.execute(sql, values)
        conn.commit()

        # Güncelleme sonrası veriyi tekrar kontrol edelim
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=400, detail="Güncelleme yapılamadı, ID hatalı olabilir."
            )

        cursor.close()
        conn.close()
        return {"status": "success", "message": "Proje başarıyla güncellendi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Güncelleme hatası: {str(e)}")
