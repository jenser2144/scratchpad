{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH toggl_task AS (

    SELECT
        id::BIGINT,
        TRIM(BOTH FROM task_name) AS task_name
    FROM
        {{ source("raw", "toggl_task") }}
)

SELECT
    *
FROM
    toggl_task