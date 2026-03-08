router = APIRouter(prefix="/api/budget")

@router.get("/list")
async def list_budget_projects():
    # ... SELECT * FROM budget_projects ...
