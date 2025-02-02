# Workflow Orchestration, Kestra, and ETL Pipelines Quiz

## Overview
This document provides answers to a set of multiple-choice questions related to workflow orchestration, Kestra, and ETL pipelines for data lakes and warehouses.

## Quiz Questions and Answers

### 1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e., the output file `yellow_tripdata_2020-12.csv` of the extract task)?
**Answer:** 128.3 MB

![Screenshot 2025-02-01 at 10 51 00 PM](https://github.com/user-attachments/assets/f58068c2-c78d-4df1-9b9f-3fbe7ff4bdbd)

### 2. What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
**Answer:** `green_tripdata_2020-04.csv`

### 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
**Answer:** 24,648,499

#### SQL Query:
```sql
SELECT count(1) FROM public.yellow_tripdata
WHERE tpep_pickup_datetime >= '2020-01-01'
AND tpep_pickup_datetime <= '2020-12-31';
```

### 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?
**Answer:** 1,734,051

#### SQL Query:
```sql
SELECT count(1) FROM public.green_tripdata
WHERE lpep_pickup_datetime >= '2020-01-01'
AND lpep_pickup_datetime <= '2020-12-31';
```

### 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
**Answer:** 1,925,152

#### SQL Query:
```sql
SELECT count(1) FROM public.yellow_tripdata
WHERE tpep_pickup_datetime >= '2021-03-01'
AND tpep_pickup_datetime <= '2021-03-31';
```

### 6. How would you configure the timezone to New York in a Schedule trigger?
**Answer:** Add a timezone property set to `America/New_York` in the Schedule trigger configuration

![Screenshot 2025-02-01 at 11 32 33 PM](https://github.com/user-attachments/assets/bcc0c75f-91c9-4dd9-8100-450bd7ced10d)


## Notes
- The answers provided are based on extracted dataset properties and execution configurations.
- Ensure that execution parameters are correctly set when running ETL workflows.

## References
- [Kestra Documentation](https://kestra.io/docs/)


