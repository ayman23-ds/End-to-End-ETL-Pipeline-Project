# End-to-End-ETL-Pipeline-Project-Using-Python


Welcome to the **End to End ETL Pipeline Project Using Python Project** repository
The goal of this project is to simulate a real world data engineering workflow  from raw data ingestion to generating meaningful business insights.

---

##  What You Will Find Here

-  Data extraction from multiple sources (API, databases, CSV files)
-  Data cleaning and validation processes
-  Data transformation and enrichment
-  Dimensional data modeling (Star Schema)
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























