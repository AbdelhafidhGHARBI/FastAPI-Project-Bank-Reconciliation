from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import reconcile
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(reconcile.router, prefix="/api/v1", tags=["reconciliation"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')
