-- Create DB
create database db;
use db;

CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_status INT,
    order_date DATE,
    required_date date,
    shipped_date date,
    store_id int,
    staff_id int,
    extraction_date bigint,
    data_source varchar(50)
    
);


CREATE TABLE order_items (
    order_id INT,
    item_id varchar(50), -- contains 4 string values ( error when loading it if the type is INT )
    product_id INT,
	quantity int,
    list_price float,
    discount float,
    extraction_date bigint,
    data_source varchar(50)
    
);

