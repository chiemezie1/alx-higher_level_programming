-- This script calculates the average temperature in Fahrenheit by city
-- and orders the results by temperature in descending order

SELECT city, AVG(temperature) AS avg_temperature
FROM temperatures
GROUP BY city
ORDER BY avg_temperature DESC;
