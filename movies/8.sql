SELECT people.name
FROM people
LEFT OUTER JOIN  stars ON (people.id = stars.person_id)
LEFT OUTER JOIN movies ON (stars.movie_id = movies.id)
WHERE movies.title="Toy Story";
