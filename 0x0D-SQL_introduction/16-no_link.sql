-- A script that lists all records of the table
--     second_table of the database in your MySQL server.

-- Don’t list rows without a name value
-- Results should display the score and the name by descending score

SELECT score, name 
FROM second_table 
WHERE name IS NOT NULL 
ORDER BY score DESC