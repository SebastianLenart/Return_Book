"""

select * from customer;
----------------------------------------------------------------------------------

SELECT
   first_name || ' ' || last_name as "Full name", -- or CONCAT
   CONCAT_WS(', ', first_name, last_name) "Full2 name",
   email
FROM
   customer
order by
first_name,
last_name desc;
----------------------------------------------------------------------------------
SELECT
	first_name,
	LENGTH(first_name) len
FROM
	customer
ORDER BY
	len DESC;
----------------------------------------------------------------------------------
select first_name from customer
order by first_name nulls first;
--Use NULLS FIRST and NULLS LAST options to explicitly
--specify the order of NULL with other non-null values.
----------------------------------------------------------------------------------
--FOREIGNKEY and REFERENCES
CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP
);
CREATE TABLE roles(
   role_id serial PRIMARY KEY,
   role_name VARCHAR (255) UNIQUE NOT NULL
);
CREATE TABLE account_roles (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  grant_date TIMESTAMP,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (role_id)
      REFERENCES roles (role_id),
  FOREIGN KEY (user_id)
      REFERENCES accounts (user_id)
);
----------------------------------------------------------------------------------
--DISCINCT
CREATE TABLE distinct_demo (
	id serial NOT NULL PRIMARY KEY,
	bcolor VARCHAR,
	fcolor VARCHAR
);
INSERT INTO distinct_demo (bcolor, fcolor)
VALUES
	('red', 'red'),
	('red', 'red'),
	('red', NULL),
	(NULL, 'red'),
	('red', 'green'),
	('red', 'blue'),
	('green', 'red'),
	('green', 'blue'),
	('green', 'green'),
	('blue', 'red'),
	('blue', 'green'),
	('blue', 'blue');
SELECT
	DISTINCT bcolor, -- rozna kombinacja ale wiersze sie powtarzaja
	fcolor
FROM
	distinct_demo
ORDER BY
	bcolor, -- DISCTINCT sie laczy z order by
	fcolor;
--------------------------
-- https://stackoverflow.com/questions/50846722/what-is-the-difference-between-postgres-distinct-vs-distinct-on
SELECT
	DISTINCT ON (bcolor) bcolor,
	fcolor
FROM
	distinct_demo
ORDER BY
	bcolor,
	fcolor;
--------------------------
SELECT
	DISTINCT ON (bcolor) *
FROM
	distinct_demo
ORDER BY
	bcolor,
	fcolor;
--SELECT a,b FROM R group by a  to samo co :
--SELECT DISTINCT on (a) a, b from r;
----------------------------------------------------------------------------------























"""