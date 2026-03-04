from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Aykor Panel API running"}

@app.get("/projects")
def get_projects():
    return [
        {"id": 1, "name": "Demo Projectsssssssss"},
        {"id": 2, "name": "Future Project"}
    ]
