
{{
    config(
        materialized='view'
    )
}}


with tripdata as 
(
  select *
  from {{ source('staging','fhv_tripdata') }}
  where dispatching_base_num is not null
)


select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    {{ dbt.safe_cast("dispatching_base_num", api.Column.translate_type('STRING')) }} as dispatchid,
    {{ dbt.safe_cast("Affiliated_base_number", api.Column.translate_type("STRING")) }} as affilid,
    {{ dbt.safe_cast("PUlocationID", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("DOlocationID", api.Column.translate_type("integer")) }} as dropoff_locationid,

    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,

    SR_Flag,

from tripdata