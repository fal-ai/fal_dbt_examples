SELECT agent_wait_time_in_minutes.business as y,
       CAST(DATE(created_at) as DATE) as ds
FROM `learning-project-305919.dbt_meder.zendesk_ticket_data`
