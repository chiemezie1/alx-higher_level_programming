-- A script that converts database to UTF8 (utf8mb4, collate utf8mb4_unicode_ci) in your MySQL server.

-- Converts following to UTF8:
--     Table first_table
--     Field name in first_table

-- Change the character set and collation of the entire database
ALTER DATABASE hbtn_0c_0
    CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Change the character set and collation of the first_table table
ALTER TABLE first_table
    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Change the character set and collation of the name field in first_table
ALTER TABLE first_table
    MODIFY name VARCHAR(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
