

{{ config(materialized='table') }}

select 
  premise_key,
  premise_code,
  premise_description
from {{ ref('stg_la_collision') }}
group by 1, 2, 3
