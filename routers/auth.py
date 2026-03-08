from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection
from typing import Optional

router = APIRouter(prefix="/api/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False # Yeni alan

@router.post("/login")
async def login(data: LoginRequest, response: Response):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not pwd_context.verify(data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

    # Çerez ömrünü belirle
    if data.remember_me:
        # 30 gün (30 gün * 24 saat * 60 dk * 60 sn)
        max_age = 30 * 24 * 60 * 60 
    else:
        # Tarayıcı kapanana kadar (None)
        max_age = None 

    response.set_cookie(
        key="user_session", 
        value=user['username'], 
        max_age=max_age,
        httponly=True # Güvenlik için: JS tarafından okunamaz
    )
    
    return {"status": "success", "user": user['full_name']}
