from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.get("/top-risk")
def top_risk_providers(limit: int = 20):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT provider_id,
                   specialty,
                   avg_complexity,
                   total_claims
            FROM provider_complexity_exposure
            ORDER BY avg_complexity DESC
            LIMIT :limit                     
    """), {"limit": limit})
        
        return [dict(row._mapping) for row in result]