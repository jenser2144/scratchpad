{{
    config(
        materialized="table",
        schema="staging"
    )
}}

WITH book_db AS (

    SELECT
        TRIM(title) AS title,
        TRIM(toggl_title) AS toggl_title,
        TRIM(author) AS author,
        TRIM(published) AS published,
        TRIM(genre_1) genre_1,
        TRIM(genre_2) AS genre_2,
        TRIM(genre_3) AS genre_3,
        TRIM(type) AS type,
        pages::integer,
        TRIM(series) AS series,
        book_num::integer,
        start_dt,
        end_dt,
        rating_goodreads::float,
        my_rating::integer,
        TRIM(read_status) AS read_status,
        TRIM(version_read) AS version_read,
        date_added
    FROM
        {{ source("raw", "book_db") }}
)

SELECT
    *
FROM
    book_db