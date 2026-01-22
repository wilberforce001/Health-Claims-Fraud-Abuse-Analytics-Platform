from fastapi import FastAPI
from app.routers import providers, cpt, risk, analytics

app = FastAPI(
    title="Health Fraud Analytics API",
    description="CPT Complexity, BETOS exposure, and provider risk analytics",
    version="1.0.0"
)

app.include_router(providers.router, prefix="/providers", tags=["Providers"])
app.include_router(cpt.router, prefix="/cpt", tags=["CPT"])
app.include_router(risk.router, prefix="/risk", tags=["Risk"])
app.include_router(analytics.router)

@app.get("/")
def health_check():
    return {"status": "ok"}