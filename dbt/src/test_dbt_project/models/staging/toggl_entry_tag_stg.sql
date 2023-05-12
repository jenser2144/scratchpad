{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH toggl_entry_tag AS (

    SELECT
        id::BIGINT,
        toggl_entry_id::BIGINT,
        toggl_tag_id::BIGINT
    FROM
        {{ source("raw", "toggl_entry_tag") }}
)

SELECT
    *
FROM
    toggl_entry_tag