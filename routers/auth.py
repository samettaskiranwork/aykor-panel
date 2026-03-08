from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection
from typing import Optional

router = APIRouter(prefix="/api/auth")

# passlib'i bcrypt ile uyumlu çalışacak şekilde ayarlıyoruz
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

        # 1. Kullanıcı var mı kontrolü
        if not user:
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 2. KRİTİK DÜZELTME (Truncate): 
        # Yeni bcrypt kütüphanesinin çökmesini engellemek için şifreyi 72 karakterle sınırlıyoruz.
        # Bu işlem senin 8 karakterlik şifreni bozmaz, sadece kütüphaneyi sakinleştirir.
        safe_password = data.password[:72]

        # 3. Şifre Doğrulama
        try:
            is_valid = pwd_context.verify(safe_password, user['password_hash'])
        except ValueError as e:
            # Eğer hala hata verirse loglara detay yazdırıp 500 dönelim
            print(f"Kütüphane Hatası: {str(e)}")
            raise HTTPException(status_code=500, detail="Güvenlik kütüphanesi hatası")

        if not is_valid:
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 4. Giriş Başarılı: Çerez (Cookie) Ayarları
        max_age = 30 * 24 * 60 * 60 if data.remember_me else None
        response.set_cookie(
            key="user_session", 
            value=user['username'], 
            max_age=max_age,
            httponly=True,
            samesite="lax"
        )
        
        return {"status": "success", "user": user['full_name']}

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Genel Hata: {str(e)}")
        raise HTTPException(status_code=500, detail="Sunucu tarafında bir hata oluştu")
