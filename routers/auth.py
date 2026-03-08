from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection
from typing import Optional

router = APIRouter(prefix="/api/auth")

# bcrypt ayarlarını passlib üzerinden tanımlıyoruz
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

        # 1. KULLANICI KONTROLÜ
        if not user:
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 2. KRİTİK DÜZELTME: BCrypt 72 byte limitini aşmamak için şifreyi kırpıyoruz
        # Bu işlem passlib'in yeni bcrypt sürümleriyle çökmesini engeller
        safe_password = data.password[:72]

        # 3. ŞİFRE DOĞRULAMA
        if not pwd_context.verify(safe_password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 4. ÇEREZ (COOKIE) AYARLARI
        # Beni hatırla seçildiyse 30 gün, seçilmediyse tarayıcı kapanana kadar
        max_age = 30 * 24 * 60 * 60 if data.remember_me else None

        response.set_cookie(
            key="user_session", 
            value=user['username'], 
            max_age=max_age,
            httponly=True,   # Güvenlik için: Tarayıcı tarafındaki JS bu çerezi okuyamaz
            samesite="lax"   # Modern tarayıcılarda yönlendirme güvenliği için
        )
        
        return {"status": "success", "user": user['full_name']}

    except Exception as e:
        # Hata detayını Render loglarında görmek için print ekledik
        print(f"Giriş Hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Sunucu tarafında bir hata oluştu")
