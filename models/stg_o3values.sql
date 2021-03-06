WITH o3values as
  (SELECT *
   FROM `bigquery-public-data.epa_historical_air_quality.o3_daily_summary`),
     counties as
  (SELECT *
   FROM {{ ref('stg_counties') }})

SELECT MAX(o3values.first_max_value) as O3,
       o3values.state_name as state,
       o3values.county_name as county,
       DATE_TRUNC(o3values.date_local, MONTH) as month,
       ANY_VALUE(counties.county_geom) as geom
FROM o3values
LEFT JOIN counties on CONCAT(o3values.state_code, o3values.county_code) = counties.county_fips_code
WHERE o3values.date_local >= DATE('2016-01-01')
GROUP BY 2,
         3,
         4
