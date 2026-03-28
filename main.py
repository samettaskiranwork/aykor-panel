from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# 1. IMPORT DÜZELTMESİ (Doğru Klasör Yapısı)
from sunucu_isleri import (
    projects, budget, future, firms, 
    suppliers, auth, home_api, 
    project_list_api, add_project_api, edit_projects
)
from database import get_db_connection 

app = FastAPI()

# 2. STATİK DOSYALAR (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. ŞABLON (HTML) YOLU (Klasör Yapısına Uygun)
base_path = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(base_path, "static", "pages"))

# Routerları bağla
app.include_router(projects.router)
app.include_router(budget.router)
app.include_router(future.router)
app.include_router(firms.router)
app.include_router(suppliers.router)
app.include_router(home_api.router)
app.include_router(project_list_api.router)
app.include_router(add_project_api.router)
app.include_router(auth.router)
app.include_router(edit_projects.router)

@app.get("/", response_class=HTMLResponse)
async def serve_login(request: Request):
    if request.cookies.get("user_session"):
        return RedirectResponse(url="/home")
    
    # GÜNCEL YAZIM: Parametreleri isimlendirerek gönderiyoruz
    return templates.TemplateResponse(
        request=request,
        name="login/login.html",
        context={}
    )

@app.get("/home", response_class=HTMLResponse)
async def serve_home(request: Request):
    if not request.cookies.get("user_session"):
        return RedirectResponse(url="/")

    # GÜNCEL YAZIM: context içinde verileri paketliyoruz
    return templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context={"active_page": "home"}
    )

@app.get("/{page_name}", response_class=HTMLResponse)
async def serve_others(request: Request, page_name: str):
    # API isteklerini veya özel rotaları engellememek için basit bir kontrol
    if page_name.startswith("api") or "." in page_name:
        return None

    if not request.cookies.get("user_session"):
        return RedirectResponse(url="/")

    # GÜNCEL YAZIM: Sayfa adını context ile gönderiyoruz
    return templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context={"active_page": page_name}
    )