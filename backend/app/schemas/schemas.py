from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List

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
