"""

-- 4 KRK--------------------------------
---ALIASY-------------------------------
SELECT
	c.customer_id alias1,
	c.first_name as alias2,
	amount,
	payment_date
FROM
	customer c
INNER JOIN payment p
    ON p.customer_id = c.customer_id
ORDER BY
   payment_date DESC;
-----------------------------------------
  SELECT
	customer.customer_id, -- bo w obu tabelach jest ta sama kolumna
	first_name,
	last_name,
	amount,
	payment_date
FROM
	customer
INNER JOIN payment
    ON payment.customer_id = customer.customer_id
ORDER BY payment_date;
-- to co wyzej tylko z aliasami
SELECT
	c.customer_id,
	first_name,
	last_name,
	email,
	amount,
	payment_date
FROM
	customer c
INNER JOIN payment p
    ON p.customer_id = c.customer_id
WHERE
    c.customer_id = 2;
----- USING zamiast ON ...=...
SELECT
	customer_id,
	first_name,
	last_name,
	amount,
	payment_date
FROM
	customer
INNER JOIN payment USING(customer_id)
ORDER BY payment_date;
--- MULTI JOIN--------------------------
SELECT
	c.customer_id,
	c.first_name customer_first_name,
	c.last_name customer_last_name,
	s.first_name staff_first_name,
	s.last_name staff_last_name,
	amount,
	payment_date
FROM
	customer c
INNER JOIN payment p
    ON p.customer_id = c.customer_id
INNER JOIN staff s
    ON p.staff_id = s.staff_id
ORDER BY payment_date;
---- SELF JOIN--------------------------
CREATE TABLE employee (
	employee_id INT PRIMARY KEY,
	first_name VARCHAR (255) NOT NULL,
	last_name VARCHAR (255) NOT NULL,
	manager_id INT,
	FOREIGN KEY (manager_id)
	REFERENCES employee (employee_id)
	ON DELETE CASCADE
);
INSERT INTO employee (
	employee_id,
	first_name,
	last_name,
	manager_id
)
VALUES
	(1, 'Windy', 'Hays', NULL),
	(2, 'Ava', 'Christensen', 1),
	(3, 'Hassan', 'Conner', 1),
	(4, 'Anna', 'Reeves', 2),
	(5, 'Sau', 'Norman', 2),
	(6, 'Kelsie', 'Hays', 3),
	(7, 'Tory', 'Goff', 3),
	(8, 'Salley', 'Lester', 3);
-----------------
SELECT
    e.first_name || ' ' || e.last_name employee,
    m .first_name || ' ' || m .last_name manager
FROM
    employee e
INNER JOIN employee m ON m.employee_id = e.manager_id;
-----------------
SELECT
    f1.title,
    f2.title,
    f1.length
FROM
    film f1
INNER JOIN film f2
    ON f1.film_id <> f2.film_id AND
       f1.length = f2.length;
--------FULL JOIN------------------------------
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS employees;

CREATE TABLE departments (
	department_id serial PRIMARY KEY,
	department_name VARCHAR (255) NOT NULL
);
select * from departments;
CREATE TABLE employees (
	employee_id serial PRIMARY KEY,
	employee_name VARCHAR (255),
	department_id INTEGER
);
INSERT INTO departments (department_name)
VALUES
	('Sales'),
	('Marketing'),
	('HR'),
	('IT'),
	('Production');

INSERT INTO employees (
	employee_name,
	department_id
)
VALUES
	('Bette Nicholson', 1),
	('Christian Gable', 1),
	('Joe Swank', 2),
	('Fred Costner', 3),
	('Sandra Kilmer', 4),
	('Julia Mcqueen', NULL);
--------------
SELECT
	employee_name,
	department_name
FROM
	employees e
FULL OUTER JOIN departments d
        ON d.department_id = e.department_id;
-------------------
       SELECT
	employee_name,
	department_name
FROM
	employees e
FULL OUTER JOIN departments d ON d.department_id = e.department_id
WHERE
	department_name IS NULL;
---------CROSS JOIN-------------------------------------------
--- n x m rowsof tables A(n) and B(m)
DROP TABLE IF EXISTS T1;
CREATE TABLE T1 (label CHAR(1) PRIMARY KEY);

DROP TABLE IF EXISTS T2;
CREATE TABLE T2 (score INT PRIMARY KEY);

INSERT INTO T1 (label)
VALUES
	('A'),
	('B');

INSERT INTO T2 (score)
VALUES
	(1),
	(2),
	(3);
---- CROSS JOIN---
SELECT *
FROM T1
CROSS JOIN T2;
--- NATURAL JOIN ----
CREATE TABLE categories (
	category_id serial PRIMARY KEY,
	category_name VARCHAR (255) NOT NULL
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
	product_id serial PRIMARY KEY,
	product_name VARCHAR (255) NOT NULL,
	category_id INT NOT NULL,
	FOREIGN KEY (category_id) REFERENCES categories (category_id)
);
INSERT INTO categories (category_name)
VALUES
	('Smart Phone'),
	('Laptop'),
	('Tablet');

INSERT INTO products (product_name, category_id)
VALUES
	('iPhone', 1),
	('Samsung Galaxy', 1),
	('HP Elite', 2),
	('Lenovo Thinkpad', 2),
	('iPad', 3),
	('Kindle Fire', 3);
-------------------------
SELECT * FROM products
NATURAL JOIN categories; --- chuj wie jak to dziala
-------------------------
SELECT	* FROM products
INNER JOIN categories USING (category_id);








"""