from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import projects, budget, future, firms, suppliers
from typing import Union # Hata almamak için bunu ekledik

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modülleri sisteme dahil ediyoruz
app.include_router(projects.router)
app.include_router(budget.router)
app.include_router(future.router)
app.include_router(firms.router)
app.include_router(suppliers.router)

# ANA SAYFA VE DİĞER SAYFALAR (F5 SORUNU İÇİN)
@app.get("/", response_class=HTMLResponse)
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
    return templates.TemplateResponse("dashboard.html", {"request": request})
