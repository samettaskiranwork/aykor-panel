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
        
        # 1. Kullanıcıyı getir
        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            print(f"DEBUG: '{data.username}' bulunamadı.")
            raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

        # 2. Şifre Doğrulama (Byte dönüşümü ve temizlik)
        try:
            # Şifreyi ve hash'i byte formatına çevir, varsa boşlukları temizle
            password_bytes = data.password.strip().encode('utf-8')
            hashed_bytes = user['password_hash'].strip().encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, hashed_bytes):
                # Başarılı
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
                print(f"DEBUG: {data.username} için şifre yanlış.")
                raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")
        
        except Exception as bcrypt_error:
            print(f"SİSTEM HATASI (Bcrypt): {str(bcrypt_error)}")
            raise HTTPException(status_code=500, detail=f"Şifre kontrol hatası: {str(bcrypt_error)}")

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"SİSTEM HATASI (Genel): {str(e)}")
        if conn: conn.close()
        raise HTTPException(status_code=500, detail=f"Sunucu Hatası: {str(e)}")
