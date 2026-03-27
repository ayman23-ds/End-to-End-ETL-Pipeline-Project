use db;

-- orders table
SELECT * FROM orders;
SELECT * FROM orders ORDER BY 1 DESC ;
SELECT COUNT(*) FROM orders; -- expected 1445

describe orders;

SELECT
    SUM(order_id IS NULL) AS null_order_id,
    SUM(customer_id IS NULL) AS null_customer_id,
    SUM(order_status IS NULL) AS null_order_status,
    SUM(order_date IS NULL) AS null_order_date,
    SUM(required_date IS NULL) AS null_required_date,
    SUM(shipped_date IS NULL) AS null_shipped_date,
    SUM(store_id IS NULL) AS null_store_id,
	SUM(staff_id IS NULL) AS null_staff_id,
    SUM(extraction_date IS NULL) AS null_extraction_date,
    SUM(Source_file IS NULL) AS null_Source_file
    
from orders;


-- order_itmes table
SELECT * FROM order_items;
SELECT * FROM order_items ORDER BY 1 DESC ;
SELECT COUNT(*) FROM order_items; -- expected 4764

describe order_items;

SELECT
    SUM(order_id IS NULL) AS null_order_id,
    SUM(item_id IS NULL) AS null_item_id,
    SUM(product_id IS NULL) AS null_product_id,
    SUM(quantity IS NULL) AS null_quantity,
    SUM(list_price IS NULL) AS null_list_price,
    SUM(discount IS NULL) AS null_discount,
    SUM(extraction_date IS NULL) AS null_extraction_date,
    SUM(Source_file IS NULL) AS null_Source_file
    
from order_items;

