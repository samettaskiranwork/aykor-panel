from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection
from typing import Optional

router = APIRouter(prefix="/api/auth")

# Şifreleme ayarlarını passlib üzerinden tanımlıyoruz
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

        # 1. Kullanıcı Kontrolü
        if not user:
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 2. KRİTİK DÜZELTME: 
        # Passlib ve Bcrypt kütüphaneleri arasındaki 72 byte çakışmasını
        # önlemek için şifreyi doğrulamaya sokmadan önce sınırlıyoruz.
        safe_password = data.password[:72]

        # 3. Şifre Doğrulama
        # Veritabanındaki özet (hash) ile kullanıcının yazdığı şifreyi kıyaslar
        if not pwd_context.verify(safe_password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 4. Giriş Başarılı: Oturum Çerezi (Cookie) Ayarları
        # Beni Hatırla işaretlendiyse 30 gün (saniye cinsinden), değilse tarayıcı kapanana kadar
        max_age = 30 * 24 * 60 * 60 if data.remember_me else None

        response.set_cookie(
            key="user_session", 
            value=user['username'], 
            max_age=max_age,
            httponly=True,  # JS tarafından erişilemez (güvenlik için)
            samesite="lax"   # Cross-site yönlendirme uyumluluğu için
        )
        
        return {"status": "success", "user": user['full_name']}

    except Exception as e:
        # Hata anında Render loglarında tam olarak ne olduğunu görebilmek için
        print(f"--- LOGIN ERROR ---: {str(e)}")
        raise HTTPException(status_code=500, detail="Sunucu tarafında bir hata oluştu")
