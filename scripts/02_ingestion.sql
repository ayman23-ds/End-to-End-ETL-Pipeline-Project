use db;
SET GLOBAL local_infile = 1;


-- orders file 

LOAD DATA LOCAL INFILE 'D:/COURSES/Data Craft/Begginer Level/Module 8-Python/Project/DB_Tables/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



-- order_items file 

LOAD DATA LOCAL INFILE 'D:/COURSES/Data Craft/Begginer Level/Module 8-Python/Project/DB_Tables/order_items.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
