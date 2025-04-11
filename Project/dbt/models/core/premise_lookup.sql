

{{ config(materialized='table') }}

select 
  premise_key,
  cast(premise_code as int) as premise_code,
  premise_description
from {{ ref('stg_la_collision') }}
where premise_code is not null or premise_description is not null
group by 1, 2, 3
