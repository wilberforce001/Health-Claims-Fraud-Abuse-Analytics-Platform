Created a virtual environment before the installation of packages to ingest medicare data: python -m venv venv (to create): source venv/Scripts/activate (to activate it).

Install the packages: pip install pandas sqlalchemy psycopg2-binary openpyxl


## Data Sources

Medicare Part B National Summary Data (CY 2024)
Source: CMS (https://data.cms.gov)

Due to size constraints, raw datasets are not included in this repository.
Download the dataset and place it in the `/data` directory before running ingestion.
