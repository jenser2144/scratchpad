{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH toggl_project AS (

    SELECT
        id::BIGINT,
        TRIM(BOTH FROM project_name) AS project_name,
        created_at_date::TIMESTAMP,
        active::BOOLEAN
    FROM
        {{ source("raw", "toggl_project") }}
)

SELECT
    *
FROM
    toggl_project