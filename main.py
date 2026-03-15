from routers import project_list_api, add_project_api
from routers import home_api
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from routers import projects, budget, future, firms, suppliers, auth # auth eklendi
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modülleri sisteme dahil ediyoruz
app.include_router(projects.router)
app.include_router(budget.router)
app.include_router(future.router)
app.include_router(firms.router)
app.include_router(suppliers.router)
app.include_router(home_api.router)
app.include_router(auth.router) # Giriş modülü eklendi

# 1. GİRİŞ SAYFASI (Adresi yazınca ilk bura açılır)
@app.get("/", response_class=HTMLResponse)
async def serve_login(request: Request):
    # Eğer kullanıcı zaten giriş yapmışsa direkt home'a gönder (Opsiyonel)
    if request.cookies.get("user_session"):
        return RedirectResponse(url="/home")
    return templates.TemplateResponse("login.html", {"request": request})

# 2. ERP ANA PANELİ VE DİĞER SAYFALAR
# Bu yolların hepsi artık dashboard.html dosyasını açar
@app.get("/home", response_class=HTMLResponse)
@app.get("/list", response_class=HTMLResponse)
@app.get("/add", response_class=HTMLResponse)
@app.get("/budget-list", response_class=HTMLResponse)
@app.get("/budget-add", response_class=HTMLResponse)
@app.get("/future-list", response_class=HTMLResponse)
@app.get("/future-add", response_class=HTMLResponse)
@app.get("/firma-list", response_class=HTMLResponse)
@app.get("/firma-add", response_class=HTMLResponse)
@app.get("/supplier-list", response_class=HTMLResponse)
@app.get("/supplier-add", response_class=HTMLResponse)
@app.get("/reports", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    # GÜVENLİK KONTROLÜ: Giriş yapmamış kişiyi login'e geri atar
    if not request.cookies.get("user_session"):
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("dashboard.html", {"request": request})
