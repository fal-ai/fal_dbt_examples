WITH o3values as
  (SELECT * FROM {{ ref('stg_o3values') }})

SELECT
    O3 as y,
    month as ds
FROM
    o3values
WHERE
    state = 'California'
    AND county = 'Los Angeles'
