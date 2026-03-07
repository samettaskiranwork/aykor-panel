from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import projects # Yeni oluşturduğumuz modül

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modülleri buraya kaydediyoruz
app.include_router(projects.router)

@app.get("/", response_class=HTMLResponse)
@app.get("/list", response_class=HTMLResponse)
@app.get("/add", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
