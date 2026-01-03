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
    
@router.get("/explanations")
def provider_explanations(limit: int = 50):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                provider_id,
                specialty,
                cpt_code,
                usage_count,
                avg_usage,
                deviation,
                complexity_score,
                risk_level,
                risk_contribution
                FROM provider_fraud_explanation
                ORDER BY risk_contribution DESC
                LIMIT :limit                          
"""), {"limit": limit})
        return [dict(row.mapping) for row in result]

