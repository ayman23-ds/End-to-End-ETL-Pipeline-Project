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

#### **Monthly Sales Analysis**
the monthly sales charts show that sales were relatively stable across most months, with normal fluctuations over time.
In general monthly sales mostly ranged between nearly 8 million and 22 million which indicates a fairly consistent sales pattern during most of the observed period.

However there is one very clear exceptional spike around November 2017 where total sales rose dramatically to nearly 88 million.
This value is far above the normal monthly range and should be highlighted as a major event in the business cycle.

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/0386231d2a97f66356880e9262ccef8c3947412b/reports/monthly_sales_line.png)
![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/0386231d2a97f66356880e9262ccef8c3947412b/reports/monthly_sales_bars.png)


### **Product and Category Performance**

#### **Top 10 Best Selling Products**

the Top 10 Products chart shows that a limited number of products contribute a very large portion of total sales.

The highest-selling product is:
- Trek Slash 8 27.5 - 2016

followed by:
- Trek Conduit+ - 2016
- Trek Fuel EX 8 29 - 2016
- Trek Domane S 5 Disc - 2017

This indicates that product sales are not equally distributed.
Instead a relatively small number of products are responsible for a large share of total revenue.

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/cb27eb5bcac7840b1184ec95d4c442010e093ddf/reports/Top_10_Products.png)

#### **Top 5 Best Selling Categories**

The Top 5 Categories chart shows that:

- Mountain Bikes is the best selling category by a large margin
- Road Bikes comes second
- Cruisers Bicycles is third
- Electric Bikes and Cyclocross Bicycles follow behind

This means customer demand is concentrated strongly in Mountain Bikes.
The gap between Mountain Bikes and the other categories is significant which suggests that this category is a major revenue driver.


![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/cb27eb5bcac7840b1184ec95d4c442010e093ddf/reports/Top_5_Categories.png)


### **Store Performance**

The store sales chart shows a very strong concentration in one store:

- Baldwin Bikes is by far the top performing store
- then come Santa Cruz Bikes and Rowlett Bikes but with a much smaller contribution

**Interpretation**

Baldwin Bikes is clearly dominating the sales landscape.
Its total sales are several times higher than the next stores which may indicate:

- better location
- larger customer base
- stronger operational performance

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/6dcdbe5a106cf8a5283aef742148de4de3973de2/reports/Top_5_Stores.png)


### **Customer Behavior Analysis**

#### **Customer Spending Distribution**

The customer spending histogram shows a right skewed distribution

This means that:
- most customers have relatively low to medium total spending
- a smaller number of customers spend very high amounts

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/633683c8aa03e59ce8e29aaeeb844c8c9c8fad86/reports/Customer_Spending_Distribution.png)

#### **Average Spending by Customer Segment**

The customer segment bar chart confirms a clear separation between three groups:
- Low segment has the smallest average spending
- Medium segment spends more around 3x the low group
- High segment spends far more than the other two groups

The average spending for the High segment is extremely larger than the other groups which confirms that the segmentation is meaningful and useful.

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/633683c8aa03e59ce8e29aaeeb844c8c9c8fad86/reports/Average_Spending_by_Customer_Segment.png)


### **Sales Distribution by Customer Locality**

The customer locality pie chart shows that sales are overwhelmingly dominated by one group:
- non local customers with value 0 represents about 98.8%
- local customers with value 1 represents only about 1.2%

**Interpretation**

This means the business is highly dependent on customers from different locations.
The other group contributes only a very small fraction of overall sales.
![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/730ecc8b5b477afa049f07c725eb359cddf381cb/reports/Customer_Locality_pie.png)

### **Delivery Performance Analysis**

**On-Time vs Late Deliveries**

The delivery performance charts show:
- around 67.9% of orders were delivered on time
- around 32.1% were delivered late

**Interpretation**

The company performs reasonably well because most orders are delivered on time.
However a late delivery rate of about one-third is still significant and may negatively affect:

- customer satisfaction
- repeat purchases
- trust in service quality

![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/730ecc8b5b477afa049f07c725eb359cddf381cb/reports/Delivery_Performance.png)
![image alt](https://github.com/ayman23-ds/End-to-End-ETL-Pipeline-Project/blob/730ecc8b5b477afa049f07c725eb359cddf381cb/reports/Delivery_Performance_pie.png)


### **Overall Findings**

Based on the charts the main findings are:

- Sales generally show stable behavior over time with one major spike in November 2017
- 2017 is the strongest sales year in the dataset
- A small number of products generate a large share of revenue
- Mountain Bikes is the leading category
- Baldwin Bikes is the top performing store by a large margin
- Customer spending is highly skewed with a small group of high value customers
- Customer segmentation clearly separates low, medium, and high spenders
- Sales are not heavily concentrated in locality customer
- About 32% of deliveries are late which indicates an important operational challenge

---

## **Final Conclusion**

The analysis demonstrates that the Gold Layer successfully supports business intelligence and reporting.
By modeling the data into a Galaxy Schema and building analytical charts the project reveals clear insights across sales, customers, products, stores, and logistics.

From a business perspective the most important opportunities are:

- focusing on top selling products and categories
- learning from the highest performing store
- retaining high value customers
- improving delivery operations
- investigating unusual sales spikes for strategic planning

Overall the project shows how raw operational data can be transformed into actionable insights through a complete ETL pipeline and dimensional modeling approach.

---
## 📁 Project Structure Summary

```
End-to-End ETL Pipeline
│
├── Data 
│   ├── raw
│   ├── intermediate
│   ├── staging_1
│   ├── staging_2
│   └── gold_layer
│
├── reports
│
└── scripts
│    ├── python scripts
│    └── sql scripts
└── 
```

---

## About Me

I am a **Data Engineer** with a strong interest in building modern data platforms and scalable data pipelines.

I am currently pursuing a **Master’s degree in Machine Learning and Deep Learning at the University of Pavia, Italy**. My academic and technical focus includes:

* Data Engineering & Data Warehousing
* ETL / ELT Pipelines
* Big Data Technologies
* Machine Learning & Deep Learning

I am passionate about designing efficient data architectures that enable advanced analytics and intelligent systems.

## Connect With Me

🔗 [LinkedIn Profile](https://www.linkedin.com/in/ahmed-ayman-b69219354/)






















