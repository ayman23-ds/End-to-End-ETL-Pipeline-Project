# End-to-End-ETL-Pipeline-Project-Using-Python


Welcome to the **End to End ETL Pipeline Project Using Python Project** repository
The goal of this project is to simulate a real world data engineering workflow  from raw data ingestion to generating meaningful business insights.

---

##  What You Will Find Here

-  Data extraction from multiple sources (API, databases, CSV files)
-  Data cleaning and validation processes
-  Data transformation and enrichment
-  Dimensional data modeling (Galaxy Schema)
-  Business insights through data visualization

---

##  Project Purpose

This project is designed to:

- Build strong foundations in **Data Engineering**
- Practice **real world ETL pipelines**
- Understand how raw data becomes **actionable insights**

---

##  Technologies Used

- Python (Pandas, NumPy, requests, SqlAlchemy, Mysql.connector, glop, os )
- SQL (MySQL)
- Data Visualization (Matplotlib / Seaborn)

---

##  Final Output

- Clean and structured datasets
- Data warehouse (Fact & Dimension tables)
- Insightful charts and reports

---
##  Model Architecture
![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/aa7903311280db714b8c7f9148407f43ec375970/reports/data_flow.png)

- **Bronze Layer**: Stores raw data as is from the source systems. Data is ingested from CSV Files, API, DB into MYSQL Database.
- **Silver Layer**: This layer includes data cleansing, standardization, and normalization processes to prepare data for analysis.
- **Gold Layer**: Houses business ready data modeled into a Galaxy schema required for reporting and analytics.

---
## Data Extraction
the first step in this project is **data extraction** , where raw data is collected from multiple resources

### Data Sources
the project integrates data from three main sources : 

- **API**
  External data is fetched using `requests` library to get currency exchange rates from open exchange rates API.
  the result is saved in csv file named : currency.csv

- **Realation Database**
  data is extracted from structured tables in `MYSQL RDBMS` such as orders, order items tables
  this operation was done using mysql.connector in python to establish a connection with db. 
  the result is saved in csv files named : orders.csv , order_items.csv.

- **Data Lake (Local Files)**
  Multiple CSV files are loaded from local directories:
  the result is saved in csv files named :brands.csv , categories.csv, customers.csv, products.csv , staffs.csv , stocks.csv , stores.csv

---
## 🥉 Bronze Layer

The **Bronze Layer** represents the raw ingestion stage of the pipeline.  
At this stage, all extracted data is stored in its original format with minimal transformation.

- Read all datasets using Python (`pandas`, `glob`, `os`)
- Standardize file formats and naming conventions
- Add metadata columns:
  - `extraction_timestamp`
  - `extraction_date`
  - `data_source`
- Keep data in raw format without applying business logic
- All datasets are stored in the `Bronze layer`.

---

## 🥈 Silver Layer – Data Cleaning & Transformation

The **Silver Layer** focuses on cleaning, validating, and transforming the raw data from the Bronze layer into a structured and reliable format.
At this stage, data quality is improved and business logic is applied to prepare the datasets for analytical processing.

###  Data Cleaning

The following data quality checks and cleaning steps are performed:

- Handle missing values (null checks)
- Remove duplicate records
- Validate data types (dates, numeric values, etc.)
- Fix inconsistent or incorrect values
- Ensure referential integrity between datasets


###  Data Transformation

After cleaning several transformations are applied:

- **Referential Integrity Check (Order Items vs Orders)**  
  Removed records from the `order_items` table where the `order_id` does not exist in the `orders` table.
  This step prevents orphan records and ensures reliable joins during data modeling and analysis also This ensures data consistency and guarantees that all order items are linked to valid orders.
  
- **Aggregation of Order Items**  
  Aggregated the `order_items` table to handle cases where the same `order_id` and `product_id` appear in multiple rows.  
  These rows were grouped and combined into a single record by:
  - Summing quantities  
  - Calculating total sales values  
  This ensures accurate representation of each product within an order and avoids duplication in analysis.

- **Currency Conversion**  
  Convert product prices using exchange rates from `currency.csv`

- **Delivery Metrics**  
  - Create `is_late` column to identify delayed shipments  
  - Calculate `latency_days` based on shipping and required dates  

- **Locality Flag**  
  Determine whether a customer is local to a store based on city by creating `is_local` flag.

- **Lookup Tables**  
  Replace coded values (`order status`) with descriptive labels  

- **Column Standardization**  
  Rename and reorder columns for consistency.

The cleaned and transformed datasets are stored in `silver layer`

---
## 🥇 Gold Layer – Data Modeling & Analytics

The **Gold Layer** represents the final stage of the ETL pipeline, where cleaned and transformed data is structured into a dimensional model for analysis and reporting.
At this stage data is optimized for business intelligence and decision making.

### **Galaxy Schema** 
Instead of using a single fact table a **Galaxy Schema**  is implemented.
This design includes multiple fact tables that share common dimension tables enabling more advanced and flexible analysis.
![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/a57d7e195a10a80c874e770046655e4c025bf71c/reports/galaxy_schema.png)
####  Fact Tables

- **fact_sales**
  - Contains transactional sales data
  - Metrics: quantity, gross_amount, net_amount, discount, etc.
  - Flages : is_late , is_local

- **fact_inventory**
  - Contains stock and inventory data
  - Metrics: stock quantity, availability, etc.


####  Shared Dimension Tables

 fact tables are connected to  dimensions:

- **dim_product**
- **dim_store**
- **dim_date**
- **dim_customer**
- **dim_staff**

#### Relationships

- Each fact table is linked to dimension tables using foreign keys  
- Shared dimensions allow combining multiple business processes (sales & inventory)

####  Benefits

- Enables analysis across multiple business areas (sales vs inventory)
- Improves scalability and flexibility of the data model
- Reduces redundancy by sharing dimensions

---
## Report and Analysis

### **Introduction**

This section presents the main business insights obtained from the Gold Layer after building the Galaxy Schema and generating analytical charts from fact_sales and related dimensions.
The analysis focuses on sales trends, customer behavior, delivery performance, product performance, category performance, and store contribution.
The purpose of this analysis is to transform the structured warehouse data into meaningful business insights that support decision making.

### **Sales Performance Over Time**

#### **Yearly Sales Analysis**
The best performing year was clearly 2017 with total sales almost double 2016.
This suggests that the business experienced major growth in 2017 possibly due to higher demand more successful products or stronger store performance.

Sales in 2018 are much lower than 2017 but this most likely happened because the dataset for 2018 appears to cover only part of the year not the full 12 months.

**Conclusion**
Overall the time series analysis suggests:
  - strong sales growth from 2016 to 2017
  - a major peak in late 2017

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/a386929301e7581e0ddaa5ce421bf5ee26269f88/reports/yearly_sales.png)



