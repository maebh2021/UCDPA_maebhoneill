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
# Convert API string information to JSON
data = request.json()
print(data)
# Convert data into Pandas Dataframe
df = pd.DataFrame(data)
# Get a list of all column names
print(df.columns)
# Select columns needed: time_last_update_utc, base_code, rates and save as DataFrame fx_rates
fx_rates = df[["time_last_update_utc", "base_code", "rates"]]
print(fx_rates)

# Import Sales Conversion Optimisation csv file into pandas DataFrame and take a look at data
conv_data = pd.read_csv("SalesConversionOptimisation.csv")
print(conv_data.head())
print(conv_data.info())
print(conv_data.shape)
print(conv_data.describe())
# Check for missing values
missing_values_count = conv_data.isnull().sum()
print(missing_values_count)
# The sum of missing values in all columns is "0" therefore there are no missing values in any of the columns.

# Drop duplicate Data Frame rows based on column"ad_id" as this is the only column that contains unique identifier
conv_duplicates = conv_data.drop_duplicates(subset="ad_id")
print(conv_duplicates.shape)

# Separate male and female prospects into two separate data frames.
male_prospects = conv_data[conv_data["gender"] == "M"]
female_prospects = conv_data[conv_data["gender"] == "F"]
print(male_prospects.shape)
print(female_prospects.shape)

# Index data by xyz-campaign_id and age for both male and female datasets
# Sort indexed data in ascending order by age for both male and female datasets
male_prospects_2 = male_prospects.set_index(["xyz_campaign_id", "age"])
male_prospects_age = male_prospects_2.sort_index(level=["age"])
print(male_prospects_age.head())
print(male_prospects_age.shape)

female_prospects_2 = female_prospects.set_index(["xyz_campaign_id", "age"])
female_prospects_age = female_prospects_2.sort_index(level=["age"])
print(female_prospects_age.head())
print(female_prospects_age.shape)

# Group data by xyz_campaign_id and age, and calculate sum of Impressions, Clicks,Spent
# Total Conversions and Approved Conversions for both datasets
total_male = male_prospects_age.groupby(["xyz_campaign_id", "age"]) \
[["Impressions", "Clicks", "Spent", "Total_Conversion", "Approved_Conversion"]].sum()
print(total_male)
print(total_male.shape)

total_female = female_prospects_age.groupby(["xyz_campaign_id", "age"]) \
[["Impressions", "Clicks", "Spent", "Total_Conversion", "Approved_Conversion"]].sum()
print(total_female)
print(total_female.shape)

# Iterate through both datasets to check column headings and data types.
for x in total_male:
    print(x)
for x in total_male:
    print(type(x))

for x in total_female:
    print(x)
for x in total_female:
    print(type(x))
