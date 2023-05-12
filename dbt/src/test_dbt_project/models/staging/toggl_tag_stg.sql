{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH toggl_tag AS (

    SELECT
        id::BIGINT,
        TRIM(BOTH FROM tag_name) AS tag_name
    FROM
        {{ source("raw", "toggl_tag") }}
)

SELECT
    *
FROM
    toggl_tag