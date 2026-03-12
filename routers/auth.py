from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from database import get_db_connection
from typing import Optional

router = APIRouter(prefix="/api/auth")

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False

@router.post("/login")
async def login(data: LoginRequest, response: Response):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")

        # --- DÜZ MANTIK KONTROL (Şifreleme YOK) ---
        # Veritabanındaki yazı ile formdan gelen yazı bizzat aynı mı?
        if data.password.strip() == user['password_hash'].strip():
            
            # Giriş Başarılı
            max_age = 30 * 24 * 60 * 60 if data.remember_me else None
            response.set_cookie(
                key="user_session", 
                value=user['username'], 
                max_age=max_age,
                httponly=True,
                samesite="lax"
            )
            return {"status": "success", "user": user['full_name']}
        else:
            raise HTTPException(status_code=401, detail="Şifre eşleşmedi")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sistem Hatası: {str(e)}")
