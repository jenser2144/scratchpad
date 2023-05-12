{{
    config(
        materialized="table",
        schema="consumption"
    )
}}

SELECT
    te.id,
    te.toggl_project_id,
    tp.project_name,
    te.toggl_task_id,
    tt.task_name,
    te.toggl_user_id,
    tu.name,
    te.start_date,
    te.end_date,
    te.update_date,
    EXTRACT(EPOCH FROM (te.end_date - te.start_date)) AS duration_secs,
    EXTRACT(EPOCH FROM (te.end_date - te.start_date))/60 AS duration_mins,
    EXTRACT(EPOCH FROM (te.end_date - te.start_date))/3600 AS duration_hours,
    CAST(EXTRACT(YEAR FROM te.start_date) AS VARCHAR(4)) AS start_date_year,
    CAST(EXTRACT(YEAR FROM te.end_date) AS VARCHAR(4)) AS end_date_year
FROM
    {{ ref("toggl_entry_stg") }} te
JOIN
    {{ ref("toggl_project_stg") }} tp
ON
    te.toggl_project_id = tp.id
JOIN
    {{ ref("toggl_task_stg") }} tt
ON
    te.toggl_task_id = tt.id
JOIN
    {{ ref("toggl_user_stg") }} tu
ON
    te.toggl_user_id = tu.id