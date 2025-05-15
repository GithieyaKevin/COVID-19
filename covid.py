# importing the libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# loading the dataset

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv", parse_dates=['date'])

# Basic cleaning

df = df.dropna(subset=['continent'])  # Remove regional aggregates
df['cases_per_million'] = df['total_cases'] / (df['population'] / 1e6)
df['deaths_per_million'] = df['total_deaths'] / (df['population'] / 1e6)

# Get top 5 countries by total cases

top_countries = df.groupby('location')['total_cases'].max().nlargest(5).index

# Filter and plot

plt.figure(figsize=(12, 6))
for country in top_countries:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time (Top 5 Countries)')
plt.xlabel('Date')
plt.ylabel('Cases')
plt.legend()
plt.grid()
plt.show()

# Aggregate by continent

continent_stats = df.groupby('continent').agg({
    'people_fully_vaccinated_per_hundred': 'max',
    'deaths_per_million': 'max'
}).dropna()

# Plot

continent_stats.plot(kind='bar', subplots=True, figsize=(12, 8))
plt.suptitle('Vaccination vs. Death Rates by Continent')
plt.tight_layout()
plt.show()

# Aggregate daily global cases
map_df = df.groupby(['date', 'location', 'iso_code']).agg({
    'total_cases': 'max',
    'population': 'max'
}).reset_index()