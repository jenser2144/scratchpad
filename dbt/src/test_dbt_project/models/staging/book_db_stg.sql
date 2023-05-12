{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH book_db AS (

    SELECT DISTINCT
        TRIM(BOTH FROM title) AS title,
        TRIM(BOTH FROM toggl_title) AS toggl_title,
        TRIM(BOTH FROM author) AS author,
        TRIM(BOTH FROM published) AS published,
        TRIM(BOTH FROM genre_1) genre_1,
        TRIM(BOTH FROM genre_2) AS genre_2,
        TRIM(BOTH FROM genre_3) AS genre_3,
        TRIM(BOTH FROM type) AS type,
        pages::int,
        TRIM(BOTH FROM series) AS series,
        book_num::float,
        start_dt::date,
        end_dt::date,
        rating_goodreads::float,
        my_rating::float,
        TRIM(BOTH FROM read_status) AS read_status,
        TRIM(BOTH FROM version_read) AS version_read
    FROM
        {{ source("raw", "book_db") }}
)

SELECT
    *
FROM
    book_db