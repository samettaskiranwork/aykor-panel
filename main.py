from fastapi import FastAPI

app = FastAPI()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/projects")
def get_projects():
    return [
        {"id": 1, "name": "Demo Projectsssssssss"},
        {"id": 2, "name": "Future Project"}
    ]
