SELECT movies.title
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
JOIN ratings ON movies.id = ratings.movie_id
WHERE people.name IN ("Bradley Cooper", "Jennifer Lawrence")
GROUP BY movies.title
HAVING COUNT(DISTINCT stars.person_id) = 2;
