from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.get("/providers")
def provider_risk(limit: int = 20):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
              provider_id,
              fraud_risk_score
            FROM provider_fraud_score
            ORDER BY fraud_risk_score DESC
            LIMIT :limit
        """), {"limit": limit})

        return [dict(row._mapping) for row in result]
