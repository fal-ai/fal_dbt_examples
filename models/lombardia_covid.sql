{{ config(materialized='table') }}

WITH source_data as (
    select * from {{ ref('covid19_italy_region') }}
)

SELECT
    NewPositiveCases as y,
    Date as ds
FROM
    source_data
WHERE
    RegionCode = 3