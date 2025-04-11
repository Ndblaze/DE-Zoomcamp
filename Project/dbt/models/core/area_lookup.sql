
{{
    config(
        materialized='table'
    )
}}

select 
  area_key,
  cast(area_id as int) as area_id,
  area_name
from {{ ref('stg_la_collision') }}
group by 1, 2, 3
