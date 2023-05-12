{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH toggl_user AS (

    SELECT
        id::BIGINT,
        TRIM(BOTH FROM name) AS name
    FROM
        {{ source("raw", "toggl_user") }}
)

SELECT
    *
FROM
    toggl_user