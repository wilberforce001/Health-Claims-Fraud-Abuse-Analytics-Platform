from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_cpt_codes():
    return {"message": "CPT endpoint working"}
