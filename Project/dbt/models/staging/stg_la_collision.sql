
{{
    config(
        materialized='view'
    )
}}

with traffic_collisions as 
(
  select *,
    row_number() over(partition by dr_number, date_occurred) as rn
  from {{ source('staging', 'traffic_collisions') }}
  where dr_number is not null
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['dr_number', 'date_occurred']) }} as collision_id,

    -- timestamps
    cast(date_reported as timestamp) as date_reported,
    cast(date_occurred as timestamp) as date_occurred,
    cast(lpad(cast(time_occurred as string), 4, '0') as time) as time_occurred, -- safer formatting

    -- categorical lookup references
    {{ dbt_utils.generate_surrogate_key(['area_id', 'area_name']) }} as area_key,
    {{ dbt_utils.generate_surrogate_key(['crime_code', 'crime_code_description']) }} as crime_key,
    {{ dbt_utils.generate_surrogate_key(['premise_code', 'premise_description']) }} as premise_key,

    -- other fields
    mo_codes,
    area_id,
    area_name,
    crime_code,
    crime_code_description,
    premise_code,
    premise_description,
    victim_age,
    victim_sex,
    victim_descent,
    address,
    cross_street,
    location,
    reporting_district,
    cast(zip_codes as numeric) as zip_codes,
    cast(census_tracts as numeric) as census_tracts,
    cast(precinct_boundaries as numeric) as precinct_boundaries,
    cast(la_specific_plans as numeric) as la_specific_plans,
    cast(council_districts as numeric) as council_districts,
    cast(neighborhood_councils__certified_ as numeric) as neighborhood_councils__certified_

from traffic_collisions
where rn = 1

{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}
