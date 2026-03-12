from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import bcrypt
from database import get_db_connection
from typing import Optional

router = APIRouter(prefix="/api/auth")

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False

@router.post("/login")
async def login(data: LoginRequest, response: Response):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            print(f"DEBUG: '{data.username}' kullanıcısı bulunamadı.")
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # Şifreleri temizle ve byte formatına çevir
        password_bytes = data.password.strip().encode('utf-8')
        hashed_from_db = user['password_hash'].strip().encode('utf-8')

        # BCrypt kontrolü (HTTPException fırlatmadan önce sonucu bir değişkene alıyoruz)
        try:
            is_correct = bcrypt.checkpw(password_bytes, hashed_from_db)
        except Exception as e:
            print(f"SİSTEM HATASI (Bcrypt Format): {str(e)}")
            raise HTTPException(status_code=500, detail="Veritabanındaki şifre formatı hatalı!")

        if is_correct:
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
            # ŞİFRE YANLIŞSA BURAYA DÜŞER
            print(f"DEBUG: {data.username} için hatalı şifre denemesi.")
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

    except HTTPException as he:
        raise he  # Hatalı şifre uyarısını olduğu gibi fırlat
    except Exception as e:
        if conn: conn.close()
        print(f"SİSTEM HATASI (Genel): {str(e)}")
        raise HTTPException(status_code=500, detail="Sunucu hatası")
