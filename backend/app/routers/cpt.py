from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PaginatedResponse, CPTComplexityOut

router = APIRouter()


@router.get(
    "/high-risk",
    response_model=PaginatedResponse[CPTComplexityOut]
)
def high_risk_cpts(
    min_complexity: int = 4,
    risk_level: str | None = None,
    rbcs_category: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    base_query = """
        FROM cpt_complexity_view
        WHERE complexity_score >= :min_complexity
    """  
    params = {"min_complexity": min_complexity}

    if risk_level:
        base_query += " AND risk_level = :risk_level"
        params["risk_level"] = risk_level

    if rbcs_category:
        base_query += " AND rbcs_cat_desc = :rbcs_category"
        params["rbcs_category"] = rbcs_category

    total = db.execute(
        text(f"SELECT COUNT(*) {base_query}"),
        params
    ).scalar()

    result = db.execute(
        text(f"""
            SELECT
                cpt_code,
                rbcs_id,
                rbcs_cat_desc,
                complexity_score,
                risk_level,
                total_claims,
                avg_claim_amount
            {base_query}
            ORDER BY complexity_score DESC, total_claims DESC
            LIMIT :limit OFFSET :offset
        """),
        {**params, "limit": limit, "offset": offset}
    )

    return {
        "total": total,
        "items": result.mappings().all()
    }


@router.get("/complexity")
def cpt_complexity(
    min_score: int = 3,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
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
        """),
        {"min_score": min_score, "limit": limit}
    )

    return result.mappings().all()
