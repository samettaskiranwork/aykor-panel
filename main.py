from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# 1. IMPORT DÜZELTMESİ: routers -> sunucu_isleri
from sunucu_isleri import (
    projects,
    budget,
    future,
    firms,
    suppliers,
    auth,
    home_api,
    project_list_api,
    add_project_api,
    edit_projects,
)
from database import get_db_connection

app = FastAPI()

# 2. STATİK DOSYALAR (CSS, JS) BURADAN OKUNACAK
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. ŞABLON (HTML) YOLU DÜZELTMESİ
# Artık templates klasörü yok, her şey static/pages altında!
base_path = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(base_path, "static", "pages"))

# Routerları bağla
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
    # login.html artık login klasörünün içinde!
    return templates.TemplateResponse("login/login.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def serve_home(request: Request):
    if not request.cookies.get("user_session"):
        return RedirectResponse(url="/")

    # dashboard.html artık dashboard klasörünün içinde!
    return templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request, "active_page": "home"}
    )


@app.get("/edit_project/{project_id}", response_class=HTMLResponse)
async def serve_edit_project(request: Request, project_id: int):
    # Giriş kontrolü (Senin diğer rotalardaki mantığınla aynı)
    if not request.cookies.get("user_session"):
        return RedirectResponse(url="/")

    # Burada yine dashboard.html'i dönüyoruz çünkü sayfa yapın onun üzerine kurulu
    return templates.TemplateResponse(
        "dashboard/dashboard.html",
        {
            "request": request,
            "active_page": "edit_project",  # JS tarafı bunu görüp edit sayfasını yükleyecek
        },
    )


@app.get("/{page_name}", response_class=HTMLResponse)
async def serve_others(request: Request, page_name: str):
    if not request.cookies.get("user_session"):
        return RedirectResponse(url="/")
    # Klasör yapısına göre yolu güncelledik
    return templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request, "active_page": page_name}
    )
