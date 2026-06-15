-- ================================================
-- Zomato Data Analysis - SQL Business Queries
-- Author: Yash Chavan | VIT Pune CSE-DS 2024-28
-- ================================================

-- Q1: Restaurant Type Distribution
SELECT listed_type,
       COUNT(*) AS total_restaurants,
       ROUND(AVG(rate), 2) AS avg_rating
FROM bengaluru
GROUP BY listed_type
ORDER BY total_restaurants DESC;

-- Q2: Top 10 Locations by Rating
SELECT location,
       COUNT(*) AS total_restaurants,
       ROUND(AVG(rate), 2) AS avg_rating
FROM bengaluru
GROUP BY location
HAVING total_restaurants >= 50
ORDER BY avg_rating DESC
LIMIT 10;

-- Q3: Online Order Impact
SELECT CASE WHEN online_order = 1
            THEN 'Has Online Order'
            ELSE 'No Online Order' END AS order_type,
       COUNT(*) AS total,
       ROUND(AVG(rate), 2) AS avg_rating
FROM bengaluru
GROUP BY online_order;

-- Q4: Table Booking Analysis
SELECT CASE WHEN book_table = 1
            THEN 'Table Booking'
            ELSE 'No Booking' END AS booking_type,
       COUNT(*) AS total,
       ROUND(AVG(rate), 2) AS avg_rating,
       ROUND(AVG(cost_for_two), 2) AS avg_cost
FROM bengaluru
GROUP BY book_table;

-- Q5: Cuisine Performance
SELECT TRIM(SUBSTR(cuisines, 1,
       INSTR(cuisines || ',', ',') - 1)) AS primary_cuisine,
       COUNT(*) AS total,
       ROUND(AVG(rate), 2) AS avg_rating
FROM bengaluru
GROUP BY primary_cuisine
HAVING total >= 100
ORDER BY avg_rating DESC
LIMIT 10;

-- Q6: Expansion Recommendation
SELECT location,
       COUNT(*) AS restaurant_count,
       ROUND(CAST(SUM(votes) AS FLOAT)/COUNT(*), 0)
           AS votes_per_restaurant,
       ROUND(AVG(rate), 2) AS avg_rating
FROM bengaluru
GROUP BY location
HAVING restaurant_count >= 30
ORDER BY votes_per_restaurant DESC
LIMIT 15;
