WITH o3values as
  (SELECT * FROM `{{ env_var('GCLOUD_PROJECT') }}.{{ env_var('BQ_DATASET') }}.raw_o3_values`)

SELECT
    O3 as y,
    month as ds
FROM
    o3values
WHERE
    state = 'Florida'
    AND county = 'Miami-Dade'
