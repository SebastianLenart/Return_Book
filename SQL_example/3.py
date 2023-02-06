"""
--test Krk
--JOIN-----------------------------------------------------------
CREATE TABLE basket_a (
    a INT PRIMARY KEY,
    fruit_a VARCHAR (100) NOT NULL
);

CREATE TABLE basket_b (
    b INT PRIMARY KEY,
    fruit_b VARCHAR (100) NOT NULL
);

INSERT INTO basket_a (a, fruit_a)
VALUES
    (1, 'Apple'),
    (2, 'Orange'),
    (3, 'Banana'),
    (4, 'Cucumber');

INSERT INTO basket_b (b, fruit_b)
VALUES
    (1, 'Orange'),
    (2, 'Apple'),
    (3, 'Watermelon'),
    (4, 'Pear');
------- INNER JOIN -----------------------------------------------------
   SELECT
    a "AA",
    fruit_a "FRUIT_A",
    basket_b.b,
    basket_b.fruit_b
FROM
    basket_a
INNER JOIN basket_b
    ON fruit_a = fruit_b;
------- LEFT JOIN -----------------------------------------------------
  SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
LEFT JOIN basket_b
   ON fruit_a = fruit_b;
----------------
  SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
LEFT JOIN basket_b -- left outer JOIN
    ON fruit_a = fruit_b
WHERE b IS NULL;
---------- to samo co wyzej
  SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
left OUTER JOIN basket_b -- left outer JOIN
    ON fruit_a = fruit_b
WHERE b IS NULL;
------- RIGHT JOIN -----------------------------------------------------
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
RIGHT JOIN basket_b ON fruit_a = fruit_b;
---FULL OUTER JOIN -----------------------------------------
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
FULL OUTER JOIN basket_b
    ON fruit_a = fruit_b;
 --- OSTATNIE---------------------------
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
FULL JOIN basket_b
   ON fruit_a = fruit_b
WHERE a IS NULL OR b IS NULL;




"""