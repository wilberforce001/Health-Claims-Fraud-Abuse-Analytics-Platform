from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.peer import PeerComparisonOut
from sqlalchemy import text
from typing import List

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get(
    "/peer-comparison",
    response_model=List[PeerComparisonOut]
)
def peer_comparison(
    specialty: str | None = None,
    min_percentile: float = Query(0.9, ge=0, le=1),
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = """
    SELECT *
    FROM provider_peer_comparison_strict
    WHERE peer_percentile >= :min_percentile
    """

    if specialty:
        query += " AND specialty = :specialty"

    query += """
    ORDER BY peer_percentile DESC
    LIMIT :limit OFFSET :offset
    """

    params = {
        "min_percentile": min_percentile,
        "limit": limit,
        "offset": offset,
    }

    if specialty: 
        params["specialty"] = specialty

    result = db.execute(text(query), params).mappings().all()
    return result