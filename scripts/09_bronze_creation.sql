use db;

CREATE TABLE silver_orders (
    order_id INT,
    customer_id INT,
    order_status INT,
    status_name varchar(50),
    order_date DATE,
    required_date date,
    shipped_date date,
    is_late int,
    latency_days int,
    store_id int,
    staff_id int,
    is_local_city int,
    is_local_state int,
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_order_items (
    order_id INT,
    product_id INT,
    quantity int,
    list_price float,
    list_price_egp float,
    discount float,
    item_id varchar(50),
	extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_brands (
    brand_id INT,
    brand_name varchar(50),
	extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_categories (
    category_id INT,
    category_name varchar(50),
	extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_customers (
    customer_id INT,
    first_name varchar(50),
    last_name varchar(50),
    phone varchar(50),
    email varchar(50),
    street varchar(50),
    city varchar(50),
	state varchar(50),
    zip_code VARCHAR(20),
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_products (
    product_id INT,
    product_name varchar(100),
    brand_id INT,
    category_id INT,
    model_year int,
    list_price float,
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_staffs (
    staff_id INT,
	first_name varchar(50),
    last_name varchar(50),
    email varchar(50),
    phone varchar(50),
    active int,
    store_id int,
    manager_id int,
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);


CREATE TABLE silver_stocks (
    store_id INT,
    product_id INT,
    quantity INT,
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_stores (
    store_id INT,
    store_name varchar(50),
	phone varchar(50),
    email varchar(50),
    street varchar(50),
    city varchar(50),
	state varchar(50),
    zip_code VARCHAR(20),
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);

CREATE TABLE silver_currency (
    currency varchar(10),
    rate float,
    base varchar(10),
    extraction_timestamp bigint,
    extraction_date datetime,
    data_source varchar(50)
);



