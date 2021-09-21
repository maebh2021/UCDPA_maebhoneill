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

# Iterate through both datasets to check column headings.
for x in total_male:
    print(x)

for x in total_female:
    print(x)


rate_conversion_male = total_male["%_Conversion"] = (total_male["Approved_Conversion"] / total_male["Total_Conversion"])*100
rate_conversion_female = total_female["%_Conversion"] = (total_female["Approved_Conversion"] / total_female["Total_Conversion"])*100
clicks_impression_male = total_male["%clicks_impression"] = (total_male["Clicks"] / total_male["Impressions"])*100
clicks_impression_female = total_female["%clicks_impression"] = (total_female["Clicks"] / total_female["Impressions"])*100
cost_per_app_conv_male = total_male["cost_per_conv"] = (total_male["Spent"] / total_male["Approved_Conversion"])
cost_per_app_conv_female = total_female["cost_per_conv"] = (total_female["Spent"] / total_female["Approved_Conversion"])
cost_per_impression_male = total_male["cost_per_impression"] = (total_male["Spent"] / total_male["Impressions"])
cost_per_impression_female = total_female["cost_per_impression"] = (total_female["Spent"] / total_female["Impressions"])
print(total_male)
print(total_male.shape)
print(total_female)
print(total_female.shape)

# Define a custom function to return how many days are in a particular month or if a year is a leap year.
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(year):
    """ Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year, month):
    """Return number of days in that month in that year"""
    if not 1 <= month <= 12:
        return "Invalid Month"

    if month == 2 and is_leap(year):
        return 29

    return month_days[month]


# Check if 2017 is leap year
print(is_leap(2017))
# Check how many days were in February 2020
print(days_in_month(2020, 2))

# Merge databases containing multi-index using suffixes to label as Male "_M" and Female "_F"
merged_data = total_male.merge(total_female, on=["xyz_campaign_id", "age"], suffixes=["_M", "_F"])
print(merged_data)
print(merged_data.columns.values)

# Subset total_male data set by ages and plot to create 3 smaller datasets to plot.
# Plot % Conversion of each campaign by age creating a separate line-graph for each gender

df = total_male.reset_index()
M_CID_916 = df.iloc[0:4]
print(M_CID_916)
M_CID_936 = df.iloc[4:8]
print(M_CID_936)
M_CID_1178 = df.iloc[8:12]
print(M_CID_1178)

fig, ax = plt.subplots()
ax.plot(M_CID_916["age"], M_CID_916["%_Conversion"], color="b", linestyle="-.", marker="o", label="Campaign ID 916")
ax.plot(M_CID_936["age"], M_CID_936["%_Conversion"], color="navy", linestyle="--", marker="o", label="Campaign ID 936")
ax.plot(M_CID_1178["age"], M_CID_1178["%_Conversion"], color="deepskyblue", linestyle=":", marker="o", label="Campaign ID 1178")
ax.legend()
ax.set_xlabel("Age range-Male")
ax.set_ylabel("% Conversion")
ax.set_title("% Conversion rate in males by age and campaign")
plt.show()

# Subset Female data set by ages and plot.
df2 = total_female.reset_index()
F_CID_916 = df2.iloc[0:4]
print(F_CID_916)
F_CID_936 = df2.iloc[4:8]
print(F_CID_936)
F_CID_1178 = df2.iloc[8:12]
print(F_CID_1178)

fig, ax = plt.subplots()
ax.plot(F_CID_916["age"], F_CID_916["%_Conversion"], color="m", linestyle="-.", marker="o", label="Campaign ID 916")
ax.plot(F_CID_936["age"], F_CID_936["%_Conversion"], color="indigo", linestyle="--", marker="o", label="Campaign ID 936")
ax.plot(F_CID_1178["age"], F_CID_1178["%_Conversion"], color="deeppink", linestyle=":", marker="o", label="Campaign ID 1178")
ax.legend()
ax.set_xlabel("Age range-Female")
ax.set_ylabel("% Conversion")
ax.set_title("% Conversion rate in females by age and campaign")
plt.show()
