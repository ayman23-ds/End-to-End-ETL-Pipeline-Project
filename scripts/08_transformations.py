import pandas as pd
from glob import glob
import os

# ====================================
#           Import Files
# ====================================
files = glob("../data/staging_1/*.csv")
df_names = []

for i in files:
    # import file
    df = pd.read_csv(i)

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
#           Cuurency Conversion
# ====================================

usd_to_egp = df_currency.loc[df_currency["Currency"] == "EGP", "Rate"].iloc[0]

df_order_items["list_price_egp"] = df_order_items["list_price"] * usd_to_egp

col = df_order_items.pop("list_price_egp")
df_order_items.insert(4, "list_price_egp", col)

df_order_items["list_price_egp"] = df_order_items["list_price_egp"].round(2)

print("Order Items Table After USD TO EGP Transformations:")
print()
print(df_order_items)
print("=" * 50)


# ====================================
#           Delivery Metrics
# ====================================

df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
df_orders["required_date"] = pd.to_datetime(df_orders["required_date"])
df_orders["shipped_date"] = pd.to_datetime(df_orders["shipped_date"])

print('Late Delivers : ')
print()
print(df_orders[df_orders["required_date"] < df_orders["shipped_date"]])

df_orders["Is_Late"] = (df_orders["required_date"] < df_orders["shipped_date"]).astype(int)
col = df_orders.pop("Is_Late")
df_orders.insert(6, "Is_Late", col)

df_orders["latency_days"] = (df_orders["shipped_date"] - df_orders["required_date"]).dt.days
df_orders["latency_days"] = df_orders["latency_days"].where(df_orders["latency_days"] > 0, 0)
col = df_orders.pop("latency_days")
df_orders.insert(7, "latency_days", col)

print("Orders Table After Delivery Transformations :")
print()
print(df_orders)
print("=" * 50)

# ====================================
#           Locality Flag 
# ====================================

# Join Orders with Customers

df_orders = df_orders.merge(
    df_customers[['customer_id','city','state']],
    on = 'customer_id',
    how = 'left' ,
)

# Join Orders with Stores

df_orders = df_orders.merge(
    df_stores[['store_id','city','state']],
    on = 'store_id',
    how = 'left' ,
    suffixes = ('_customer','_store')
)

df_orders['IS_Local_city'] = (
    df_orders["city_customer"].str.strip().str.lower() ==
    df_orders["city_store"].str.strip().str.lower()  
    ).astype(int)

df_orders['IS_Local_state'] = (
    df_orders["state_customer"].str.strip().str.lower() ==
    df_orders["state_store"].str.strip().str.lower() 
    ).astype(int)

del df_orders['city_customer']
del df_orders['state_customer']
del df_orders['city_store']
del df_orders['state_store']

col = df_orders.pop("IS_Local_city")
df_orders.insert(10, "IS_Local_city", col)

col = df_orders.pop("IS_Local_state")
df_orders.insert(11, "IS_Local_state", col)

print("Orders Table After Locality Transformation :")
print()
print(df_orders)
print("=" * 50)


# ====================================
#           Status Lookup Table 
# ====================================

status_lookup_table = pd.DataFrame({
    "order_status": [1, 2, 3, 4],
    "status_name": ["Pending", "Processing", "Rejected", "Completed"]
})

df_orders = df_orders.merge(
    status_lookup_table,
    on = 'order_status',
    how = 'left'   
)

col = df_orders.pop("status_name")
df_orders.insert(3, "status_name", col)

print("Orders Table After Status Lookup Transformation :")
print()
print(df_orders)
print("=" * 50)


# ====================================
#           Export Files 
# ====================================

for name in df_names:
    df = globals()[name]
    
    clean_name = name.replace("df_","")
    
    df.to_csv(f"../data/staging_2/{clean_name}.csv", index=False)
    print(f" saved : {clean_name}.csv")

print()
print("Files Were Saved")
print("=" * 50)

