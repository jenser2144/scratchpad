{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH toggl_entry AS (

    SELECT
        id::BIGINT,
        toggl_project_id::BIGINT,
        toggl_task_id::BIGINT,
        toggl_user_id::BIGINT,
        start_date::TIMESTAMP,
        end_date::TIMESTAMP,
        update_date::TIMESTAMP
    FROM
        {{ source("raw", "toggl_entry") }}
)

SELECT
    *
FROM
    toggl_entry