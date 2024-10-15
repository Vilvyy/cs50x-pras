SELECT people.name
FROM people
LEFT OUTER JOIN  stars ON (people.id = stars.person_id)
LEFT OUTER JOIN movies ON (stars.movie_id = movies.id)
WHERE movies.year=2004
ORDER BY people.birth;
