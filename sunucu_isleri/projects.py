from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import get_db_connection

router = APIRouter(prefix="/api/projects")


# 1. VERİ MODELİ: Kullanıcının formdan gönderdiği yapı
class ProjectCreate(BaseModel):
    project_code: str
    priority: int  # 1-10 arası
    customer_groups: str  # customer_groups tablosundan group_name
    customer: str  # customers tablosundan customer_name
    subject: str
    item_quantity: int
    deadline: Optional[str] = None
    proengineer: str  # users tablosundan full_name
    project_type: str  # 'System' veya 'Spare Part'


# --- YARDIMCI FONKSİYONLAR: Dropdown (Açılır Menü) Verileri ---


@router.get("/get-dropdowns")
async def get_form_dropdowns():
    """Formdaki seçim kutularını doldurmak için tüm verileri tek seferde getirir"""
    try:
        conn = get_db_connection()
        # Not: Eğer veritabanı sürücün destekliyorsa cursor(dictionary=True)
        # kullanmak işi daha da kolaylaştırır ama standart cursor üzerinden gidiyorum:
        cursor = conn.cursor()

        # Müşteri Grupları
        cursor.execute("SELECT group_name FROM customer_groups")
        groups = [row[0] for row in cursor.fetchall()]

        # Müşteriler
        cursor.execute("SELECT customer_name FROM customers")
        customers = [row[0] for row in cursor.fetchall()]

        # --- MÜHENDİSLER (PE) - BURASI DEĞİŞTİ ---
        # Hem tam ismi hem de veritabanına kaydedilecek kısa ismi çekiyoruz
        cursor.execute("SELECT full_name, short_name FROM users")
        rows = cursor.fetchall()

        # JavaScript'in kolayca okuyabilmesi için liste içersinde sözlük (JSON) yapısına çeviriyoruz
        engineers = [
            {"full_name": row[0], "short_name": row[1]}
            for row in rows
            if row[1]  # short_name boş olanları almamak için önlem
        ]
        # ----------------------------------------

        cursor.close()
        conn.close()

        return {
            "groups": groups,
            "customers": customers,
            "engineers": engineers,  # Artık bu bir obje listesi: [{"full_name": "...", "short_name": "..."}, ...]
            "project_types": ["System", "Spare Part"],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Dropdown verileri çekilemedi: {str(e)}"
        )


# --- ANA FONKSİYONLAR ---


@router.get("/")
async def list_projects():
    """Tüm projeleri listeler"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM projects ORDER BY id DESC"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add")
async def create_project(project: ProjectCreate):
    """Yeni projeyi veritabanına kaydeder"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO projects 
                 (project_code, priority, customer_group, customer, subject, 
                  item_quantity, deadline, proengineer, project_type) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (
            project.project_code,
            project.priority,
            project.customer_groups,
            project.customer,
            project.subject,
            project.item_quantity,
            project.deadline,
            project.proengineer,
            project.project_type,
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{item_id}")
async def get_single_project(item_id: int):
    """Düzenleme için tek bir projenin verisini getirir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        if not item:
            raise HTTPException(status_code=404, detail="Proje bulunamadı")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/{item_id}")
async def update_project(item_id: int, project: ProjectCreate):
    """Mevcut projeyi günceller"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE projects SET 
                 project_code=%s, priority=%s, customer_group=%s, customer=%s, 
                 subject=%s, item_quantity=%s, deadline=%s, proengineer=%s, 
                 project_type=%s WHERE id=%s"""

        values = (
            project.project_code,
            project.priority,
            project.customer_groups,
            project.customer,
            project.subject,
            project.item_quantity,
            project.deadline,
            project.proengineer,
            project.project_type,
            item_id,
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# routers/projects.py içine eklenecekler:


@router.get("/get/{project_id}")
async def get_project(project_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        cursor.close()
        conn.close()
        if not project:
            raise HTTPException(status_code=404, detail="Proje bulunamadı")
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/{project_id}")
async def update_project(project_id: int, data: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE projects SET 
            subject=%s, customer=%s, item_quantity=%s, 
            priority=%s, deadline=%s, deadline_time=%s, 
            proengineer=%s, prostatus=%s, tender_reference=%s, annodate=%s
            WHERE id=%s
        """
        values = (
            data.get("subject"),
            data.get("customer"),
            data.get("item_quantity"),
            data.get("priority"),
            data.get("deadline"),
            data.get("deadline_time"),
            data.get("proengineer"),
            data.get("prostatus"),
            data.get("tender_reference"),
            data.get("annodate"),
            project_id,
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
