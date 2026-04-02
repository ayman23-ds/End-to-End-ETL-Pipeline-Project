from sqlalchemy import create_engine
from mysql.connector import Error
import pandas as pd
from glob import glob
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# ========================================================================
#                           Import Files
# ========================================================================
files = glob("../data/gold_layer/*.csv")
df_names = []

for i in files:
    # import file
    df = pd.read_csv(i)

    # change name of df
    file_name = os.path.basename(i)
    file_name = file_name.replace(".csv", "")
    globals()[f"{file_name}"] = df

    # add to list
    df_names.append(f"{file_name}")

    # print new name
    print(f"Created: {file_name}")
print()
print("Num of files",len(df_names))
print("=" * 50)


# ========================================================================
#                           Sales Over Time (Yearly)
# ========================================================================

fact_sales["order_date"] = pd.to_datetime(
    fact_sales["order_date_key"].astype(str),
    format="%Y%m%d"
)
fact_sales = fact_sales.set_index("order_date")
yearly_sales = fact_sales["net_amount"].resample("YE").sum()
plt.figure(figsize=(8,5))
bars = plt.bar(yearly_sales.index.astype(str), yearly_sales.values, edgecolor="black")

plt.title("Total Sales by Year")
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.grid(axis="y", alpha=0.3)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig("../output/yearly_sales.png", dpi=300, bbox_inches="tight")
#plt.show()

# ========================================================================
#                           Sales Over Time (Mothly)
# ========================================================================

fact_sales["order_date"] = pd.to_datetime(
    fact_sales["order_date_key"].astype(str),
    format="%Y%m%d"
)

fact_sales = fact_sales.set_index("order_date")
monthly_sales = fact_sales["net_amount"].resample("ME").sum()


fig, ax = plt.subplots(figsize=(14,6))
ax.plot(monthly_sales.index, monthly_sales.values, marker="o", linewidth=2)
ax.set_title("Sales Over Time (Monthly)")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))   
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../output/monthly_sales_line.png", dpi=300, bbox_inches="tight")
#plt.show()




fig, ax = plt.subplots(figsize=(14,6))
ax.bar(monthly_sales.index, monthly_sales.values, width=20, edgecolor="black")
ax.set_title("Monthly Sales")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("../output/monthly_sales_bars.png", dpi=300, bbox_inches="tight")
#plt.show()


# ========================================================================
#                           Top Selling Products
# ========================================================================
fact_with_products = fact_sales.merge(
    dim_products[["product_id", "product_name","category_name"]],
    on="product_id",
    how="left"
)

top_products = fact_with_products.groupby("product_name")["net_amount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
plt.barh(top_products.index, top_products.values)
plt.title("Top 10 Best Selling Products")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.savefig("../output/Top_10_Products.png", dpi=300, bbox_inches="tight")
#plt.show()

# ========================================================================
#                           Top Selling Categories
# ========================================================================
top_category = fact_with_products.groupby("category_name")["net_amount"].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(12,6))
plt.barh(top_category.index, top_category.values)
plt.title("Top 5 Best Selling categories")
plt.xlabel("Total Sales")
plt.ylabel("Category")
plt.gca().invert_yaxis()
plt.savefig("../output/Top_5_Categories.png", dpi=300, bbox_inches="tight")
#plt.show()


# ========================================================================
#                           Top Selling Stores
# ========================================================================
fact_with_stores = fact_sales.merge(
    dim_stores[["store_id", "store_name"]],
    on="store_id",
    how="left"
)

store_sales = (
    fact_with_stores
    .groupby("store_name")["net_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_stores = store_sales.head(5)

plt.figure(figsize=(10,6))
plt.barh(top_stores.index, top_stores.values)
plt.title("Top 5 Stores by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Store")
plt.gca().invert_yaxis() 
plt.grid(axis="x", alpha=0.3)
plt.savefig("../output/Top_5_Stores.png", dpi=300, bbox_inches="tight")
#plt.show()

# ========================================================================
#                           Customer Segmentation
# ========================================================================

customer_sales = fact_sales.groupby("customer_id")["net_amount"].sum()

threshold = customer_sales.quantile(0.99)
filtered_customer_sales = customer_sales[customer_sales <= threshold]

plt.figure(figsize=(12,6))
plt.hist(filtered_customer_sales, bins=20, edgecolor="black")
plt.title("Customer Spending Distribution ")
plt.xlabel("Total Spending")
plt.ylabel("Number of Customers")
plt.grid(axis="y", alpha=0.3)
plt.savefig("../output/Customer_Spending_Distribution.png", dpi=300, bbox_inches="tight")
#plt.show()



customer_sales = fact_sales.groupby("customer_id")["net_amount"].sum().reset_index()
customer_sales.columns = ["customer_id", "total_spending"]

customer_sales["segment"] = pd.qcut(
    customer_sales["total_spending"],
    q=3,
    labels=["Low", "Medium", "High"]
)

print(customer_sales.groupby("segment")["total_spending"].agg(["min", "max", "mean", "count"]))
segment_avg = customer_sales.groupby("segment")["total_spending"].mean()

plt.figure(figsize=(8,5))
plt.bar(segment_avg.index, segment_avg.values, edgecolor="black")
plt.title("Average Spending by Customer Segment")
plt.xlabel("Segment")
plt.ylabel("Average Spending")
plt.grid(axis="y", alpha=0.3)
plt.savefig("../output/Average_Spending_by_Customer_Segment.png", dpi=300, bbox_inches="tight")
#plt.show()


# ========================================================================
#                           Delivery Performance
# ========================================================================

late_counts = fact_sales["is_late"].value_counts().sort_index()
late_counts.index = ["On Time", "Late"]

plt.figure(figsize=(8,5))
plt.bar(late_counts.index, late_counts.values, edgecolor="black")
plt.title("On-Time vs Late Deliveries")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Orders")
plt.grid(axis="y", alpha=0.3)
plt.savefig("../output/Delivery_Performance.png", dpi=300, bbox_inches="tight")
#plt.show()



plt.figure(figsize=(6,6))
plt.pie(
    late_counts.values,
    labels=late_counts.index,
    autopct="%1.1f%%",   
    startangle=90        
)
plt.title("On-Time vs Late Deliveries")
plt.savefig("../output/Delivery_Performance_pie.png", dpi=300, bbox_inches="tight")
#plt.show()


# ========================================================================
#                           Customer Locality
# ========================================================================

locality_sales = fact_sales.groupby("is_local")["net_amount"].sum()
fact_sales["is_local"] = fact_sales["is_local"].replace({
    1: "Local",
    0: "Non-Local"
})


plt.figure(figsize=(6,6))
plt.pie(
    locality_sales.values,
    labels=locality_sales.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "black"}
)

plt.title("Sales Distribution by Customer Locality")
plt.savefig("../output/Customer_Locality_pie.png", dpi=300, bbox_inches="tight")
#plt.show()