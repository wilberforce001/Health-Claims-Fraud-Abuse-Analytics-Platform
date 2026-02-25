# Week 1 
## (19/02/2026)
1. What is a B-tree index?
2. How PostgreSQL uses indexes
3. What a sequential scan is
4. What an index scan is

## (20/02/2026)
1. Composite indexes
https://planetscale.com/learn/courses/mysql-for-developers/indexes/primary-key-data-types


## Checking for statistical validity in the system
### Check for NULLs


## Command to check all views in the system - List all views:
- SELECT viewname FROM pg_catalog.pg_views WHERE schemaname = 'public';
- \dv: list all views.
- \dv+: list all views with extra details lise size and description. 
- \d claims: see the actual names of the columns in the claims table. 

## PROBLEM ENCOUNTERED:
There was perfect mathematical uniformity in the dataset structure making fraud detection fail. For fraud detection to succeed, there has to be variance hence the need to introduce statistical variation. I, therefore, had to fix the data generator to:
- Randomize the number of CPTs per provider
- Randomize the number of claims per CPT
- Introduce heavy-tail distribution
- Add a few high-volume "outlier" providers

