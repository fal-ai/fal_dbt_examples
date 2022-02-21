-- source table contains zendesk ticket data
-- more info: https://developer.zendesk.com/api-reference/ticketing/tickets/ticket_metrics/

SELECT agent_wait_time_in_minutes.business as y,
       CAST(DATE(created_at) as DATE) as ds
FROM `{{ env_var('GCLOUD_PROJECT') }}.{{ env_var('BQ_DATASET') }}.zendesk_ticket_metric_data`
