
{{ config(
    materialized='table'
) }}

WITH monthly_rev AS (
    SELECT 
        a.service_type, 
        b.year, 
        b.month, 
        b.quarter, 
        SUM(a.total_amount) AS monthly_revenue
    FROM 
        {{ ref("fact_trips") }} AS a
    LEFT JOIN 
        {{ ref("dim_taxi_dates") }} AS b
    ON 
        EXTRACT(YEAR FROM a.pickup_datetime) = b.year
        AND EXTRACT(MONTH FROM a.pickup_datetime) = b.month
    GROUP BY 
        a.service_type, 
        b.year, 
        b.month, 
        b.quarter
)

SELECT * 
FROM monthly_rev
ORDER BY year, month

