use db;

CREATE TABLE fact_sales (
    sales_key INT,
    order_id INT,
	item_id INT,
    customer_id INT, 
    product_id INT,
    store_id int,
    staff_id int,
    
    order_status varchar(50),
    order_date_key int,
    required_date_key int,
    shipped_date_key int,
    is_late int,
    latency_days int,
    is_local int,
    
    quantity int,
    list_price_egp float,
    discount float,
    gross_amount float,
    net_amount float

);

CREATE TABLE fact_inventory (
	inventory_key int,
    store_id INT,
    product_id INT,
    quantity INT,
	date date,
    date_key int
);




CREATE TABLE dim_products (
    product_id INT,
    product_name varchar(100),
    brand_id INT,
    brand_name varchar(50),
    category_id INT,
    category_name varchar(50),
    model_year int
);


CREATE TABLE dim_staffs (
    staff_id INT,
	full_name varchar(100),
    email varchar(50),
    phone varchar(50),
    is_active int,
    store_id int,
    manager_id int

);

CREATE TABLE dim_stores (
    store_id INT,
    store_name varchar(50),
	phone varchar(50),
    email varchar(50),
    street varchar(50),
    city varchar(50),
	state varchar(50),
    zip_code VARCHAR(20)
);


CREATE TABLE dim_customers (
    customer_id INT,
    full_name varchar(100),
    phone varchar(50),
    email varchar(50),
    street varchar(50),
    city varchar(50),
	state varchar(50),
    zip_code VARCHAR(20)
);

CREATE TABLE dim_date (
	date_key INT,
    full_date date,
    year INT,
    quarter INT,
	month INT,
	month_name varchar(20),
    day INT,
	day_name varchar(20),
    is_weekend varchar(20)
);



