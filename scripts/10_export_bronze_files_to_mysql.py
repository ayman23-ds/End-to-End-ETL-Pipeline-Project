from sqlalchemy import create_engine
from mysql.connector import Error
import pandas as pd
from glob import glob
import os

# ====================================
#           Import Files
# ====================================
files = glob("../data/staging_2/*.csv")
df_names = []

for i in files:
    # import file
    df = pd.read_csv(i)
    df["extraction_date"] = pd.to_datetime(df["extraction_date"])
    
    # change name of df
    file_name = os.path.basename(i)
    file_name = file_name.replace(".csv", "")
    globals()[f"df_{file_name}"] = df

    # add to list
    df_names.append(f"df_{file_name}")

    # print new name
    print(f"Created: df_{file_name}")
print()
print("Num of files",len(df_names))
print("=" * 50)

# ====================================
#           Prepare Data
# ====================================

df_orders["order_date"] = pd.to_datetime(df_orders["order_date"]).dt.date
df_orders["required_date"] = pd.to_datetime(df_orders["required_date"]).dt.date
df_orders["shipped_date"] = pd.to_datetime(df_orders["shipped_date"]).dt.date


print()
print("Orders Table Info : ")
print(df_orders.info())
print("=" * 50)

# ====================================
#           Prepare tables
# ====================================

tables = {
    "silver_orders": df_orders,
    "silver_order_items": df_order_items,
    "silver_brands": df_brands,
    "silver_categories": df_categories,
    "silver_customers": df_customers,
    "silver_products": df_products,
    "silver_staffs": df_staffs,
    "silver_stocks": df_stocks,
    "silver_stores": df_stores,
    "silver_currency": df_currency
}

print()
print("Dict for Tabels")
print(tables.keys())
print("=" * 50)

# ====================================
#           Connection With MySql
# ====================================

engine = create_engine("mysql+pymysql://root:PASS@localhost/db")
print("Connected successfully")

for table_name, df in tables.items():
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"{table_name} loaded successfully")
