/* Author @Cody Torgerson

for Plista Analytics Coding Challenge


Solution Part 1 Question 1
Query to Find the name of the actor who has appeared in the most films
and how many appearances where there*/

SELECT first_name, last_name, count(film_actor.actor_id) as Total_Film_APP
From actor
inner join film_actor on actor.actor_id = film_actor.actor_id
group by (film_actor.actor_id)
order by count(film_actor.actor_id) desc
limit 1
;

/* Answer to Part 1 Question 2
Which Store had the longest rental, what was the customers name, 
and what movie did they rent for so long? */
SELECT store.store_id, timediff(return_date,rental_date)as Total_Rental_Time, first_name, last_name, title as Movie_Title FROM customer
inner join rental ON customer.customer_id = rental.customer_id
inner join inventory on rental.inventory_id = inventory.inventory_id
inner join store on inventory.store_id = store.store_id
inner join film_text on inventory.film_id = film_text.film_id
group by (Total_Rental_Time)
order by Total_Rental_Time desc
limit 2
;
/*Solution to Part 1 Question 3
What are the top 5 films by running time (descending) per film category? 
(please use the film name and category name, not IDs). 
Bonus points for converting the running time to hours and minutes! 
*/
SELECT 
    title,
    CONCAT(length DIV 60, ':',(TIME_FORMAT(length % 60, '%s'))) AS Film_Runtime,
    category.name AS Genre
   
FROM
    film 
		inner JOIN film_category ON film.film_id = film_category.film_id
		inner JOIN category ON film_category.category_id = category.category_id
		group by Film_Runtime with rollup
		Order by Genre, Film_Runtime desc
;


