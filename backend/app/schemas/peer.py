from pydantic import BaseModel, ConfigDict

class PeerComparisonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider_id: int
    specialty: str
    cpt_code: str
    usage_count: int
    risk_contribution: float
    peer_rank: int
    peer_percentile: float
    peer_group_size: int 


    