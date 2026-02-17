from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.reconciliation import ReconciliationService
from app.schemas.transaction import ReconciliationResult

router = APIRouter()

@router.post("/reconcile", response_model=ReconciliationResult)
async def reconcile(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        content = await file.read()
        return ReconciliationService.process_bank_statement(content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
