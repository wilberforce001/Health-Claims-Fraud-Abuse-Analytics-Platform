from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def risk_health():
    return {"status": "risk service ok"}