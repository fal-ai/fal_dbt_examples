{{ config(materialized='table') }}

WITH source_data as (
    select * from {{ ref('city_temperature') }}
)

SELECT
    AvgTemperature as y,
    a as x
FROM
    source_data
WHERE
    City = 'New Orleans'