# NYC Green Taxi Data Ingestion

This guide provides instructions for setting up the environment and ingesting NYC Green Taxi trip data and taxi zone data into a PostgreSQL database.

## Prerequisites

Ensure you have the following installed on your machine:
- Docker
- Python (with necessary libraries installed, e.g., `psycopg2`, `pandas`)

---

## Steps

### 1. Run Docker Compose

Start the PostgreSQL database using Docker Compose:

```bash
docker compose up
```

# 2. Ingest Green Taxi Trip Data

Download and ingest the Green Taxi trip data into the PostgreSQL database.

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url=${URL}



# 3. Ingest Green Taxi Zone Data
Download and ingest the green taxi zone lookup data into the database:

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=green_taxi_zones \
  --url=${URL}


# SQL Queries: 

## Question 3: Trip Segmentation Count

This document contains SQL queries to calculate the count of green taxi trips segmented by trip distance for October 2019.
Queries

### 1. Trips with Distance Up to 1 Mile

```sql
SELECT count(trip_distance) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' 
  AND lpep_dropoff_datetime < '2019-11-01'
  AND trip_distance <= 1;
```

### 2. Trips with Distance Between 1 (Exclusive) and 3 Miles (Inclusive)

```sql
SELECT count(trip_distance) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' 
  AND lpep_dropoff_datetime < '2019-11-01'
  AND trip_distance > 1 AND trip_distance <= 3;
```


### 3. Trips with Distance Between 3 (Exclusive) and 7 Miles (Inclusive)

```sql
SELECT count(trip_distance) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' 
  AND lpep_dropoff_datetime < '2019-11-01'
  AND trip_distance > 3 AND trip_distance <= 7;
```

### 4. Trips with Distance Between 7 (Exclusive) and 10 Miles (Inclusive)

```sql
SELECT count(trip_distance) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' 
  AND lpep_dropoff_datetime < '2019-11-01'
  AND trip_distance > 7 AND trip_distance <= 10;
```

### 5. Trips with Distance Greater Than 10 Miles
```sql
SELECT count(trip_distance) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' 
  AND lpep_dropoff_datetime < '2019-11-01'
  AND trip_distance > 10;
```


## Question 4: Finding the Pickup Time of the Longest Trip

**Query:**

```sql
SELECT lpep_pickup_datetime
FROM green_taxi_trips
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_trips);
```

## Question 5: Identifying Pickup Locations with High Total Revenue on October 18, 2019

**Query:**

```sql
SELECT * 
FROM (
  SELECT SUM(total_amount) AS total, "PULocationID"
  FROM green_taxi_trips 
  WHERE lpep_pickup_datetime >= '2019-10-18'
    AND lpep_pickup_datetime < '2019-10-19'
  GROUP BY "PULocationID"
) AS t
LEFT JOIN green_taxi_zones z
ON t."PULocationID" = z."LocationID"
WHERE t.total > 13000;
```

## Question 6: Finding the Drop-off Zone with the Largest Tip for "East Harlem North" in October 2019

**Query:**

```sql
SELECT z."Zone"
FROM green_taxi_trips t
LEFT JOIN green_taxi_zones z
ON t."DOLocationID" = z."LocationID"
WHERE t."PULocationID" = 74 -- code for East Harlem North
  AND lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime <= '2019-10-31'
  AND t.tip_amount = (
    SELECT MAX(t2.tip_amount)
    FROM green_taxi_trips t2
    WHERE t2."PULocationID" = 74
      AND t2.lpep_pickup_datetime >= '2019-10-01'
      AND t2.lpep_pickup_datetime <= '2019-10-31'
  );
```
