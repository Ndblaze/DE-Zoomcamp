
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
        service_type, 
        year, 
        quarter, 
        quarterly_revenue, 
        LAG(quarterly_revenue) OVER (
            PARTITION BY service_type, quarter ORDER BY year ASC
        ) AS prev_year_revenue,
        -- Calculate YoY growth percentage
        ROUND(
            SAFE_DIVIDE(
                quarterly_revenue - LAG(quarterly_revenue) OVER (
                    PARTITION BY service_type, quarter ORDER BY year ASC
                ), 
                LAG(quarterly_revenue) OVER (
                    PARTITION BY service_type, quarter ORDER BY year ASC
                )
            ) * 100, 2
        ) AS yoy_growth
    FROM quarterly_rev
),

ranked_growth AS (
    -- Rank best & worst quarters for 2020
    SELECT 
        service_type, 
        year, 
        quarter, 
        yoy_growth,
        RANK() OVER (PARTITION BY service_type ORDER BY yoy_growth DESC) AS best_rank,
        RANK() OVER (PARTITION BY service_type ORDER BY yoy_growth ASC) AS worst_rank
    FROM yoy_growth
    WHERE year = 2020
)

SELECT 
    service_type,
    CONCAT(CAST(year AS STRING), '/Q', CAST(quarter AS STRING)) AS quarter_label,
    yoy_growth,
    CASE WHEN best_rank = 1 THEN 'best' END AS best_quarter,
    CASE WHEN worst_rank = 1 THEN 'worst' END AS worst_quarter
FROM ranked_growth
WHERE best_rank = 1 OR worst_rank = 1
