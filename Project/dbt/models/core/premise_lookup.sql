

{{ config(materialized='table') }}

select 
  premise_key,
  cast(premise_code as int) as premise_code,
  premise_description
from {{ ref('stg_la_collision') }}
group by 1, 2, 3
