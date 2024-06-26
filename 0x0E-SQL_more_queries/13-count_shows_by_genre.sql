-- A script that lists all genres from hbtn_0d_tvshows and displays the number of shows linked to each.

-- Each record displays: <TV Show genre> - <Number of shows linked to this genre>
--     First column must be called genre
--     Second column must be called number_of_shows
-- Don’t display a genre that doesn’t have any shows linked
-- Results sorted in descending order by the number of shows linked

SELECT tv_genres.name AS genre, COUNT(*) AS number_of_shows
FROM tv_genres
INNER JOIN tv_show_genres
WHERE tv_genres.id = tv_show_genres.genre_id
GROUP BY genre
ORDER BY number_of_shows DESC
