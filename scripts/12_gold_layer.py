from sqlalchemy import create_engine
from mysql.connector import Error
import pandas as pd
from glob import glob
import os

# ========================================================================
#           Import Files
# ========================================================================
files = glob("../data/staging_2/*.csv")
df_names = []

for i in files:
    # import file
    df = pd.read_csv(i)
    df["extraction_date"] = pd.to_datetime(df["extraction_date"])
    del df['extraction_timestamp']
    del df['data_source']
    
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

# ========================================================================
#           Dim Product (products,brands,categories)
# ========================================================================

dim_products=df_products.merge(
    df_brands[['brand_name','brand_id']],
    on = 'brand_id',
    how = 'left'
    
).merge(
    df_categories[['category_name','category_id']],
    on = 'category_id',
    how = 'left'
)

usd_egp = df_currency.loc[
    df_currency['Currency'] == 'EGP',
    'Rate'
    ].iloc[0]


col = dim_products.pop("brand_name")
dim_products.insert(3, "brand_name", col)

col = dim_products.pop("category_name")
dim_products.insert(5, "category_name", col)

del dim_products['list_price']
del dim_products['extraction_date']

print()
print("Dim Products: \n")
print(dim_products)
print("=" * 50)


# ========================================================================
#                              Dim Staff
# ========================================================================

dim_staffs = df_staffs.copy()

col = dim_staffs.pop("active")
dim_staffs.insert(5, "is_active", col)

dim_staffs["full_name"] = dim_staffs['first_name'].fillna('') + " " + dim_staffs["last_name"].fillna('')

col = dim_staffs.pop("full_name")
dim_staffs.insert(1, "full_name", col)

del dim_staffs['first_name']
del dim_staffs['last_name']
del dim_staffs['extraction_date']

print()
print("Dim Staffs: \n")
print(dim_staffs)
print("=" * 50)
# ========================================================================
#                              Dim Stores
# ========================================================================

dim_stores = df_stores.copy()

del dim_stores['extraction_date']

print()
print("Dim Stores: \n")
print(dim_stores)
print("=" * 50)
# ========================================================================
#                              Dim Customers
# ========================================================================

dim_customers = df_customers.copy()

dim_customers['full_name'] = dim_customers['first_name'].fillna('') + ' ' + dim_customers['last_name'].fillna('') 

col = dim_customers.pop('full_name')
dim_customers.insert(1,'full_name',col)

del dim_customers['first_name']
del dim_customers['last_name']
del dim_customers['extraction_date']

print()
print("Dim Customerss: \n")
print(dim_customers)
print("=" * 50)
# ========================================================================
#                              Dim Date
# ========================================================================

start_date = df_orders[["order_date", "required_date", "shipped_date"]].min().min()
end_date = '2030-01-01'

date_range = pd.date_range(start=start_date, end=end_date, freq="D")

dim_date = pd.DataFrame({"full_date": date_range})

dim_date["date_key"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)

col = dim_date.pop('date_key')
dim_date.insert(0,'date_key',col)

dim_date["year"] = dim_date["full_date"].dt.year

dim_date["quarter"] = dim_date["full_date"].dt.quarter

dim_date["month"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.month_name()

dim_date["day"] = dim_date["full_date"].dt.day
dim_date["day_name"] = dim_date["full_date"].dt.day_name()

dim_date["is_weekend"] = (dim_date["day_name"] == 'Friday').astype(int)
dim_date["is_weekend"] = dim_date["is_weekend"].replace({1: "Yes",0: "No"})

print()
print("Dim Date: \n")
print(dim_date)
print("=" * 50)

# ========================================================================
#                              Fact Sales
# ========================================================================

fact_sales = df_order_items.copy()

fact_sales = fact_sales.merge(
    df_orders[['order_id',
               'customer_id',
               'store_id',
               'staff_id',
               'status_name',
               'order_date',
               'required_date',
               'shipped_date',
               'Is_Late',
               'latency_days',
               'IS_Local_city']
            ],
    on = "order_id",
    how = "left"
)

fact_sales['order_status'] = fact_sales['status_name']

fact_sales["gross_amount"] = (fact_sales["quantity"] * fact_sales["list_price_egp"])

fact_sales["net_amount"] = (
    fact_sales["gross_amount"]  - (fact_sales["discount"] * fact_sales["list_price_egp"] )
)

fact_sales = fact_sales.rename(columns={
    "Is_Late": "is_late",
    "IS_Local_city": "is_local"
})

fact_sales = fact_sales.drop(columns=["list_price", "status_name"])

fact_sales = fact_sales [
    ["order_id",
     "item_id",
     "customer_id",
     "product_id",
     "store_id",
     "staff_id",
     "order_status",
     "order_date",
     "required_date",
     "shipped_date",
     "is_late",
     "latency_days",
     "is_local",
     "quantity",
     "list_price_egp",
     "discount",
     "gross_amount",
     "net_amount",
  
    ]
]

fact_sales["sales_key"] = range(1, len(fact_sales) + 1)

col = fact_sales.pop("sales_key")
fact_sales.insert(0, "sales_key", col)


fact_sales["order_date_key"] = pd.to_datetime(fact_sales["order_date"]).dt.strftime("%Y%m%d").astype("Int64")

fact_sales["required_date_key"] = pd.to_datetime(fact_sales["required_date"]).dt.strftime("%Y%m%d").astype("Int64")

fact_sales["shipped_date_key"] = pd.to_datetime(fact_sales["shipped_date"]).dt.strftime("%Y%m%d").astype("Int64")

fact_sales = fact_sales.drop(columns=["order_date", "required_date","shipped_date"])

col = fact_sales.pop("order_date_key")
fact_sales.insert(8, "order_date_key", col)

col = fact_sales.pop("required_date_key")
fact_sales.insert(9, "required_date_key", col)

col = fact_sales.pop("shipped_date_key")
fact_sales.insert(10, "shipped_date_key", col)

print()
print("Fact Sales: \n")
print(fact_sales)
print("=" * 50)

# ========================================================================
#                              Fact Inventory
# ========================================================================

fact_inventory = df_stocks.copy()

fact_inventory['date'] = pd.to_datetime(fact_inventory['extraction_date']).dt.normalize()
dim_date['full_date'] = pd.to_datetime(dim_date['full_date']).dt.normalize()

fact_inventory = fact_inventory.merge(
    dim_date[['date_key','full_date']],
    left_on = "date",
    right_on = "full_date",
    how = 'left'
)

fact_inventory = fact_inventory [[
    "store_id",
    "product_id",
    "quantity",
    "date",
    "date_key"
]]
fact_inventory.insert(0, "inventory_key", range(1, len(fact_inventory) + 1))

print()
print("Fact Inventory: \n")
print(fact_inventory)
print("=" * 50)
# ========================================================================
#                              Save on Folder gold_layer
# ========================================================================
fact_sales.to_csv(f"../data/gold_layer/fact_sales.csv", index=False)
print(f" saved : fact_sales.csv")
print()

fact_inventory.to_csv(f"../data/gold_layer/fact_inventory.csv", index=False)
print(f" saved : fact_inventory.csv")
print()
print('-'*20)

dim_products.to_csv(f"../data/gold_layer/dim_products.csv", index=False)
print(f" saved : dim_products.csv")
print()

dim_staffs.to_csv(f"../data/gold_layer/dim_staffs.csv", index=False)
print(f" saved : dim_staffs.csv")
print()

dim_stores.to_csv(f"../data/gold_layer/dim_stores.csv", index=False)
print(f" saved : dim_stores.csv")
print()

dim_customers.to_csv(f"../data/gold_layer/dim_customers.csv", index=False)
print(f" saved : dim_customers.csv")
print()

dim_date.to_csv(f"../data/gold_layer/dim_date.csv", index=False)
print(f" saved : dim_date.csv")
print("=" * 50)
# ========================================================================
#                              Export To Gold Layer
# ========================================================================

tables = {
    "fact_sales": fact_sales,
    "fact_inventory": fact_inventory,
    "dim_products": dim_products,
    "dim_staffs": dim_staffs,
    "dim_stores": dim_stores,
    "dim_customers": dim_customers,
    "dim_date": dim_date

}

engine = create_engine("mysql+pymysql://root:180709@localhost/db")
print("Connected successfully")

for table_name, df in tables.items():
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"{table_name} loaded successfully")