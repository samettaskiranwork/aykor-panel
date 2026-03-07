from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import projects

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Proje modülünü ana sisteme bağlıyoruz
app.include_router(projects.router)

# Link değişse bile aynı sayfayı yüklemesi için bu yolları tanımladık
@app.get("/", response_class=HTMLResponse)
@app.get("/list", response_class=HTMLResponse)
@app.get("/add", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
