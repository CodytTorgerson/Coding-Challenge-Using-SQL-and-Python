/*Concat(length div 60,":",(time_format(length % 60,"%s")))*/
SELECT 
    title,
    CONCAT(length DIV 60, ':',(TIME_FORMAT(length % 60, '%s'))) AS Film_Runtime,
    category.name AS Genre
   
FROM
    film 
	Inner JOIN film_category ON film.film_id = film_category.film_id
	INNER JOIN category ON film_category.category_id = category.category_id
	group by Film_Runtime, Genre
    Order by Film_Runtime desc, Genre desc
    limit 5,5;
    
    
   
;