# Importing basic Python libraries for data cleaning and visualisation

import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Retrieve data from online API showing daily currency fx rates for USD
request = requests.get("https://open.er-api.com/v6/latest/USD")
print(request.status_code)
print(request.text)
data = request.json()
print(data)
# Convert data into Pandas Dataframe
df = pd.DataFrame(data)
# Get a list of all column names
print(df.columns)
# Select columns needed: time_last_update_utc, base_code, rates and save as DataFrame fx_rates
fx_rates = df[["time_last_update_utc", "base_code", "rates"]]
print(fx_rates)

# Import csv file into pandas DataFrame
