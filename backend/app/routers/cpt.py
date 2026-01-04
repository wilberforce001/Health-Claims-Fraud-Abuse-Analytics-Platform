from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.get("/complexity")
def cpt_complexity(min_score: int = 3, limit: int = 50):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
              cpt_code,
              rbcs_id,
              rbcs_cat_desc,
              complexity_score,
              risk_level,
              total_claims,
              avg_claim_amount
            FROM cpt_complexity_view
            WHERE complexity_score >= :min_score
            ORDER BY complexity_score DESC, avg_claim_amount DESC
            LIMIT :limit
        """), {"min_score": min_score, "limit": limit})

        return [dict(row._mapping) for row in result]
    
    total = db.execute(text("""
SELECT COUNT (*) FROM cpt_complexity_view
WHERE complexity_score >= :min_complexity
"""), {"min_complexity": min_complexity}).scalar()
    
    return {
        "total": total,
        "items": result.mappings().all()
    }