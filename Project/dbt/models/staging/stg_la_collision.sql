 
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
    
    case
        when safe_cast(substr(lpad(cast(time_occurred as string), 4, '0'), 1, 2) as int64) between 0 and 23
        and safe_cast(substr(lpad(cast(time_occurred as string), 4, '0'), 3, 2) as int64) between 0 and 59
        then parse_time('%H:%M:%S',
            substr(lpad(cast(time_occurred as string), 4, '0'), 1, 2) || ':' ||
            substr(lpad(cast(time_occurred as string), 4, '0'), 3, 2) || ':00'
        )
        else null
    end as time_occurred,


    -- categorical lookup references
    {{ dbt_utils.generate_surrogate_key(['area_id', 'area_name']) }} as area_key,
    {{ dbt_utils.generate_surrogate_key(['crime_code', 'crime_code_description']) }} as crime_key,
    {{ dbt_utils.generate_surrogate_key(['premise_code', 'premise_description']) }} as premise_key,

    --locations json parse
    -- cast to string first in case it’s a struct, then extract as scalar
    safe_cast(JSON_EXTRACT_SCALAR(cast(location as string), '$.latitude') as float64) as latitude,
    safe_cast(JSON_EXTRACT_SCALAR(cast(location as string), '$.longitude') as float64) as longitude,

    -- creating location_point
    st_geogpoint(
    safe_cast(JSON_EXTRACT_SCALAR(cast(location as string), '$.longitude') as float64),
    safe_cast(JSON_EXTRACT_SCALAR(cast(location as string), '$.latitude') as float64)
    ) as location_point,


    -- other fields
    mo_codes,
    cast(area_id as int) as area_id,
    area_name,
    cast(crime_code as int) as crime_code,
    crime_code_description,
    cast(premise_code as int) as premise_code,
    premise_description,
    victim_age,
    victim_sex,
    victim_descent,
    address,
    cross_street,
    reporting_district,
    cast(zip_codes as numeric) as zip_codes,
    cast(census_tracts as numeric) as census_tracts,
    cast(precinct_boundaries as numeric) as precinct_boundaries,
    cast(la_specific_plans as numeric) as la_specific_plans,
    cast(council_districts as numeric) as council_districts,
    cast(neighborhood_councils__certified_ as numeric) as neighborhood_councils__certified_

from traffic_collisions
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'   this is what you use when you want to run everything
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}
