
{{
    config(
        materialized='table'
    )
}}

with fhv_tripdata as (
    SELECT
        *,
        TIMESTAMP_DIFF(dropOff_datetime, pickup_datetime, SECOND) AS trip_duration_seconds
    FROM {{ ref('dim_fhv_trips') }}
)

SELECT
    year,
    month,
    pickup_zone,
    dropoff_zone,
    PERCENTILE_CONT(trip_duration_seconds, 0.90) OVER (PARTITION BY year, month, pickup_locationid, dropoff_locationid) AS p90
FROM fhv_tripdata
ORDER BY year, month
