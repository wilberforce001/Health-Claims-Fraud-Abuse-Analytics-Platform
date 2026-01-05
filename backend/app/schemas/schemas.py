from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List
from decimal import Decimal

T = TypeVar("T")

class ProviderRiskOut(BaseModel):
    # Enable Pydantic to work with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True) 
    
    provider_id: int
    specialty: str
    avg_deviation: float
    total_claims: int

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]

class CPTComplexityOut(BaseModel):
    cpt_code: str
    rbcs_id: str | None
    rbcs_cat_desc: str | None
    complexity_score: int
    risk_level: str
    total_claims: int
    avg_claim_amount: Decimal

    class Config:
        from_attributes = True
