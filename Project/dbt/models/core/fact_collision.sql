

{{
    config(
        materialized='table'
    )
}}

with table_ids as (
    select *
    from {{ ref('stg_la_collision') }}
),

select collision_id,
       date_reported, 
       date_occurred,
       time_occurred, 
       victim_age,
       victim_sex,
       victim_descent,
       crime_code,
       location_id,
       area_id, 
       premise_id, 
       council_district_id 
    
from table_ids
