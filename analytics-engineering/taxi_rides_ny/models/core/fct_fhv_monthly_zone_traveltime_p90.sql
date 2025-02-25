{{
    config(
        materialized='table'
    )
}}

WITH fhv_tripdata AS (
    SELECT *, TIMESTAMP_DIFF(dropOff_datetime, pickup_datetime, DAY) as trip_duration
    FROM {{ ref('dim_fhv_trips') }}
)

SELECT 
    year,
    month,
    pickup_locationid,
    dropoff_locationid,
    PERCENTILE_CONT(trip_duration, 0.90) OVER (PARTITION BY year, month, pickup_locationid, dropoff_locationid) AS p90
FROM fhv_tripdata
ORDER BY year, month
