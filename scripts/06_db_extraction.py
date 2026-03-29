import mysql.connector
from mysql.connector import Error
import pandas as pd

try:
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="PASS",
        database="db",
    )

    cursor = conn.cursor()

    # Check DB

    cursor.execute("select database();")
    current_db = cursor.fetchall()
    print("Current DB Is :", current_db)
    print("-" * 30)

    # Get Tables
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    table_names = []
    print("Tables:")
    for table in tables:
        print("-", table[0])
        table_names.append(table[0])

    print("-" * 30)

    print("list table_names contain :")
    print(table_names)
    print("-" * 30)

    # Make Dataframes
    dfs = {}

    for table_name in table_names:
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
        dfs[table_name] = df
        print(f"Loaded: {table_name}, Shape: {df.shape}")

    print("-" * 30)

    # Show Tables
    print(dfs["orders"].head())
    print("-" * 30)

    print(dfs["order_items"].head())
    print("-" * 30)

    # Save Tables Into CSV Files
    dfs["orders"].to_csv("../data/intermediate/orders.csv", index=False)
    print("orders file is saved")
    print("-" * 30)

    dfs["order_items"].to_csv("../data/intermediate/order_items.csv", index=False)
    print("order_items file is saved")
    print("-" * 30)

    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print(f"Error: {e}")
