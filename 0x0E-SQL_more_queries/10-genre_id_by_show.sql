-- A script that lists all shows contained in hbtn_0d_tvshows that have at least one genre linked.

-- Each record should display: tv_shows.title - tv_show_genres.genre_id
-- Results must be sorted in ascending order by tv_shows.title and tv_show_genres.genre_id

SELECT title, genre_id
FROM hbtn_0d_tvshows
WHERE tv_show_genres.genre_id NOT NULL
ORDER BY tv_shows.title
