from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import projects, budget, future, firms # Hepsini içeri al

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Routerları Kaydet
app.include_router(projects.router)
app.include_router(budget.router)
app.include_router(future.router)
app.include_router(firms.router)

@app.get("/", response_class=HTMLResponse)
@app.get("/{path}", response_class=HTMLResponse)
async def serve_dashboard(request: Request, path: Optional[str] = "list"):
    return templates.TemplateResponse("dashboard.html", {"request": request})
