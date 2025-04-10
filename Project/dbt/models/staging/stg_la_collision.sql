
{{
    config(
        materialized='view'
    )
}}

with traffic_collisions as 
(
  select *,
    row_number() over(partition by area_id, date_occurred) as rn
  from {{ source('staging', 'traffic_collisions') }}
  where area_id is not null
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['area_id', 'date_occurred']) }} as collision_id,
    {{ dbt.safe_cast("area_id", api.Column.translate_type("integer")) }} as area_id,
    {{ dbt.safe_cast("reporting_district", api.Column.translate_type("integer")) }} as reporting_district,
    {{ dbt.safe_cast("crime_code", api.Column.translate_type("integer")) }} as crime_code,
    
    -- timestamps
    cast(date_reported as timestamp) as date_reported,
    cast(date_occurred as timestamp) as date_occurred,
    
    -- victim info
    victim_age,
    victim_sex,
    victim_descent,
    
    -- premise info
    premise_code,
    premise_description,
    
    -- location info
    address,
    cross_street,
    location,
    cast(zip_codes as numeric) as zip_codes,
    cast(census_tracts as numeric) as census_tracts,
    cast(precinct_boundaries as numeric) as precinct_boundaries,
    cast(la_specific_plans as numeric) as la_specific_plans,
    cast(council_districts as numeric) as council_districts,
    cast(neighborhood_councils__certified_ as numeric) as neighborhood_councils__certified_,
    
from traffic_collisions
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}
