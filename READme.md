# Health Insurance Claims Fraud & Abuse Detection System
## Core users
- Health insurers who need:
- - Loss modeling
- - Frequency and severity analysis
- - Risk stratification
- - Explainable models which is very important in the US. 
- Third-party administrators (TPAs)
- Self-insured employers

## Minimum Viable Product (MVP) Scope
### Fraud Types to Detect (MVP) 
These fraud types are well-documented and statistically detectable.
- Upcoding: Billing higher CPT codes than justified
- Duplicate claims: Same procedure, same patient, different dates/providers
- Outlier billing: Provider bills high frequency or cost.

### Input (Simulated or Public Data)
- CMS public claims datasets
- Synthetic claims data 

### Outputs (What makes it valuable)
- For each claim:
- - Fraud risk score (0-1)
- - Reason flags (explainability)
- - Expected financial leakage

- For providers:
- - Risk ranking 
- - Peer comparison metrics

## Actuarial Models to be employed
- Frequency modeling 
- - Poisson / Negative Binomial
- - Claims per provider per period
- Severity modeling 
- - Gamma / Lognormal
- - Claim amount distribution
- Peer Group Analysis: Compare providers by: 
- - Specialty
- - Geography
- - Patient mix
- Fraud Score (Explainable): Weighted combination of:
- - Z-scores
- - Control chart violations (SPC) for anomaly detection
- - GLM residuals
- Gradient boosting as supporting model 

## Tech Stack
### Backend 
- Python (FastAPI)
- Node for auth & APIs

### Data
- PostgreSQL
- Pandas, Numpy

### ML / Stats
- statsmodels
- scikit-learn

### Frontend
- React
- Charts: Chart.js

## Infra
- Docker
- Simple CI
- Deployed on AWS

## System Architecture
Data Ingestion  
↓  
Statistical Engine (Python)  
    ↓  
Risk Scoring Layer  
    ↓  
API (FastAPI)  
    ↓  
Dashboard (React)

