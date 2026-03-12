from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import bcrypt # passlib yerine direkt bcrypt kullanıyoruz
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
        
        # Veritabanından kullanıcıyı getir
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (data.username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        # --- HATA AYIKLAMA (Render Loglarında Gözükür) ---
        if not user:
            print(f"DEBUG: '{data.username}' kullanıcısı veritabanında bulunamadı!")
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # Şifreleri byte formatına çeviriyoruz (bcrypt bunu ister)
        password_bytes = data.password.encode('utf-8')
        hashed_bytes = user['password_hash'].encode('utf-8')

        # Şifre Doğrulama (Direkt bcrypt ile)
        if bcrypt.checkpw(password_bytes, hashed_bytes):
            # GİRİŞ BAŞARILI
            max_age = 30 * 24 * 60 * 60 if data.remember_me else None
            
            response.set_cookie(
                key="user_session", 
                value=user['username'], 
                max_age=max_age,
                httponly=True,
                samesite="lax"
            )
            print(f"DEBUG: {data.username} başarıyla giriş yaptı.")
            return {"status": "success", "user": user['full_name']}
        else:
            # ŞİFRE YANLIŞ
            print(f"DEBUG: {data.username} için şifre eşleşmedi!")
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

    except Exception as e:
        print(f"SİSTEM HATASI: {str(e)}")
        raise HTTPException(status_code=500, detail="Sunucu tarafında bir hata oluştu")
