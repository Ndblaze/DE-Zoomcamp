
{{
    config(
        materialized='table'
    )
}}


select 
  crime_key,
  crime_code,
  crime_code_description
from {{ ref('stg_la_collision') }}
group by 1, 2, 3
