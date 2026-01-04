from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import PaginatedResponse, ProviderRiskOut

router = APIRouter()

@router.get("/top-risk", response_model=PaginatedResponse[ProviderRiskOut])
def top_risk_providers(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
    ):

    total = db.execute(text("""
    SELECT COUNT(*) FROM provider_risk_summary
""")).scalar()
    
    result = db.execute(text("""
    SELECT provider_id,
        specialty,
        avg_deviation,
        total_claims
        FROM provider_risk_summary
        ORDER BY avg_deviation DESC
        LIMIT :limit OFFSET :offset
"""), {"limit": limit, "offset": offset})
    
    return {
        "total": total,
        "items": result.mappings().all()
    }