import json
import requests
import pandas as pd
from pandas import json_normalize
import time

id = "52aa6535ec61438db32f3d3f5a1af663"
parametrs = {"app_id": id}
url = "https://openexchangerates.org/api/latest.json"

# .get() method :: to send a request and recieve the replay
response = requests.get(url, parametrs)
# status_code :: attribute if returns with 200 it means that its a successful request
print(response.status_code)

data = response.json()
print(data)


df = pd.DataFrame(list(data["rates"].items()), columns=["Currency", "Rate"])
print(df.head())

df["Base"] = data["base"]
df["extraction_timestamp"] = int(time.time())
df["extraction_date"] = pd.to_datetime(data["timestamp"], unit="s")
df["data_source"] = "API"


print(df.head())


df.to_csv("../data/staging_1/currency.csv", index=False)
print("currency file was saved")
