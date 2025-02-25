{{ config(
    materialized='table'
) }}

WITH quarterly_rev AS (
    -- Compute quarterly revenue
    SELECT 
        service_type,
        EXTRACT(YEAR FROM pickup_datetime) AS year, 
        EXTRACT(QUARTER FROM pickup_datetime) AS quarter, 
        SUM(total_amount) AS quarterly_revenue
    FROM {{ ref("fact_trips") }}
    GROUP BY service_type, year, quarter
),

yoy_growth AS (
    -- Compute YoY revenue growth
    SELECT 
        q1.service_type, 
        q1.year, 
        q1.quarter, 
        q1.quarterly_revenue, 
        q2.quarterly_revenue AS prev_year_revenue,
        -- Calculate YoY growth percentage
        ROUND(
            SAFE_DIVIDE(q1.quarterly_revenue - q2.quarterly_revenue, q2.quarterly_revenue) * 100, 2
        ) AS yoy_growth
    FROM quarterly_rev q1
    LEFT JOIN quarterly_rev q2 
    ON q1.service_type = q2.service_type 
    AND q1.quarter = q2.quarter 
    AND q1.year = q2.year + 1
),

best_worst AS (
    -- Identify best & worst quarters for 2020
    SELECT 
        service_type,
        CONCAT(CAST(year AS STRING), '/Q', CAST(quarter AS STRING)) AS quarter_label,
        yoy_growth,
        -- Find the best and worst quarters per service_type
        CASE 
            WHEN yoy_growth = (SELECT MAX(yoy_growth) FROM yoy_growth y WHERE y.service_type = g.service_type AND y.year = 2020) 
            THEN 'best' 
        END AS best_quarter,
        CASE 
            WHEN yoy_growth = (SELECT MIN(yoy_growth) FROM yoy_growth y WHERE y.service_type = g.service_type AND y.year = 2020) 
            THEN 'worst' 
        END AS worst_quarter
    FROM yoy_growth g
    WHERE year = 2020
)

SELECT * FROM best_worst
WHERE best_quarter IS NOT NULL OR worst_quarter IS NOT NULL
