from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection

router = APIRouter(prefix="/api/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

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

    # Basitlik olması için şimdilik bir cookie atıyoruz
    response.set_cookie(key="user_session", value=user['username'])
    return {"status": "success", "user": user['full_name']}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("user_session")
    return {"status": "success"}
