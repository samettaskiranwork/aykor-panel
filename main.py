from pydantic import BaseModel
from typing import Optional

# Veritabanı modeline tam uyumlu Pydantic modeli
class ProjectCreate(BaseModel):
    project_code: str
    priority: Optional[int] = 2  # 1: Düşük, 2: Orta, 3: Yüksek
    customer: str
    customer_group: Optional[str] = None
    subject: str
    item_quantity: Optional[int] = 0
    deadline: Optional[str] = None
    deadline_time: Optional[str] = None
    proengineer: Optional[str] = None
    prostatus: Optional[str] = "Aktif"
    annodate: Optional[str] = None
    tender_reference: Optional[str] = None
    bid_bond: Optional[float] = 0.0

@app.post("/api/add-project")
def add_project(project: ProjectCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sütun isimleri senin DDL kodunla birebir eşlendi
        sql = """INSERT INTO projects 
                 (project_code, priority, customer, customer_group, subject, item_quantity, 
                  deadline, deadline_time, proengineer, prostatus, annodate, 
                  tender_reference, bid_bond) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            project.project_code, project.priority, project.customer, project.customer_group,
            project.subject, project.item_quantity, project.deadline, project.deadline_time,
            project.proengineer, project.prostatus, project.annodate,
            project.tender_reference, project.bid_bond
        )
        
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": "Proje başarıyla kaydedildi."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
