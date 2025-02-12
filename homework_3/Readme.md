

# Homework 3

## 1. **Creating External Table**


```sql
CREATE OR REPLACE EXTERNAL TABLE taxi-rides-ny-450705.nytaxi.external_yellow_tripdata
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://ny-taxi-data-004/yellow_tripdata_2024-01.parquet', 
    'gs://ny-taxi-data-004/yellow_tripdata_2024-02.parquet', 
    'gs://ny-taxi-data-004/yellow_tripdata_2024-03.parquet', 
    'gs://ny-taxi-data-004/yellow_tripdata_2024-04.parquet', 
    'gs://ny-taxi-data-004/yellow_tripdata_2024-05.parquet', 
    'gs://ny-taxi-data-004/yellow_tripdata_2024-06.parquet'
  ]
);
```

---

## 2. **Counting Rows in External Table**

This query counts the number of rows in the external table to get an overview of the data.

```sql
SELECT count(1) FROM taxi-rides-ny-450705.nytaxi.external_yellow_tripdata;
```

---

## 3. **Creating Regular Table from External Table**

This operation imports the external data into a regular table in BigQuery for easier querying and manipulation.

```sql
CREATE OR REPLACE TABLE taxi-rides-ny-450705.nytaxi.yellow_tripdata
AS
SELECT * FROM taxi-rides-ny-450705.nytaxi.external_yellow_tripdata;
```

---

## 4. **Counting Distinct `PULocationID` in External Table**

This query counts the distinct values of `PULocationID` (pickup location ID) in the external table.

```sql
SELECT 
  COUNT(DISTINCT PULocationID) AS distinct_PULocationIDs, 
  'External Table' AS source
FROM taxi-rides-ny-450705.nytaxi.external_yellow_tripdata;
```

---

## 5. **Counting Distinct `PULocationID` in Regular Table**

This query counts the distinct values of `PULocationID` in the regular table.

```sql
SELECT 
  COUNT(DISTINCT PULocationID) AS distinct_PULocationIDs, 
  'Regular Table' AS source
FROM taxi-rides-ny-450705.nytaxi.yellow_tripdata;
```

---

## 6. **Selecting `PULocationID` from Regular Table**

This query retrieves the `PULocationID` column from the regular table.

```sql
SELECT PULocationID 
FROM taxi-rides-ny-450705.nytaxi.yellow_tripdata;
```

---

## 7. **Selecting `PULocationID` and `DOLocationID` from Regular Table**

This query retrieves both `PULocationID` (pickup) and `DOLocationID` (drop-off) columns.

```sql
SELECT PULocationID, DOLocationID 
FROM taxi-rides-ny-450705.nytaxi.yellow_tripdata;
```

---

## 8. **Counting Rows with Zero Fare Amount**

This query counts the number of rows in the regular table where the `fare_amount` column equals zero.

```sql
SELECT COUNT(*) AS zero_fare_count
FROM taxi-rides-ny-450705.nytaxi.yellow_tripdata
WHERE fare_amount = 0;
```

---

## 9. **Creating Optimized Table with Partitioning and Clustering**

This query creates an optimized version of the regular table, partitioned by `tpep_dropoff_datetime` (drop-off datetime) and clustered by `VendorID`. This optimization improves query performance.

```sql
CREATE OR REPLACE TABLE taxi-rides-ny-450705.nytaxi.optimized_yellow_taxi
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM taxi-rides-ny-450705.nytaxi.yellow_tripdata;
```

---

## 10. **Selecting Distinct VendorIDs for Specific Date Range from Regular Table**

This query retrieves distinct `VendorID` values for records between `2024-03-01` and `2024-03-15` from the regular table.

```sql
SELECT DISTINCT VendorID
FROM taxi-rides-ny-450705.nytaxi.yellow_tripdata
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

---

## 11. **Selecting Distinct VendorIDs for Specific Date Range from Optimized Table**

This query retrieves distinct `VendorID` values for the same date range, but from the optimized table.

```sql
SELECT DISTINCT VendorID
FROM taxi-rides-ny-450705.nytaxi.optimized_yellow_taxi
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

---

