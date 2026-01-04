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
    specialty: str | None = None,
    min_avg_deviation: float | None = None,
    db: Session = Depends(get_db)
    ):

    base_query = """
    FROM provider_risk_summary
    WHERE 1=1
"""
    params = {}

    if specialty:
        base_query += "AND specialty = :specialty"
        params["specialty"] = specialty

    if min_avg_deviation is not None:
        base_query += "AND avg_deviation >= :min_avg_deviation"
        params["min_avg_deviation"] = min_avg_deviation

    # Total count for pagination
    total = db.execute(text(f"SELECT COUNT(*) {base_query}"), params).scalar()
    
    # Fetch paginated results
    result = db.execute(text(f"""
    SELECT provider_id,
        specialty,
        avg_deviation,
        total_claims
    {base_query}
        ORDER BY avg_deviation DESC
        LIMIT :limit OFFSET :offset
"""), {**params, "limit": limit, "offset": offset})
    
    return {
        "total": total,
        "items": result.mappings().all()
    }