

{{
    config(
        materialized='table'
    )
}}

select
    collision_id,
    date_reported,
    date_occurred,
    time_occurred,
    area_key,
    crime_key,
    premise_key,
    victim_age,
    victim_sex,
    victim_descent,
    mo_codes,
    address,
    cross_street,
    latitude,
    longitude,
    location_point,
    reporting_district,
    zip_codes,
    census_tracts,
    precinct_boundaries,
    la_specific_plans,
    council_districts,
    neighborhood_councils__certified_
from {{ ref('stg_la_collision') }}
