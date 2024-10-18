# Anshan & Zirui

#Library
import pandas as pd
import requests

# Read the CSV file
summary_df = pd.read_csv('../data/raw/properties_stats_unfixed.csv', low_memory=False)

def fix(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit':1,
    }
    response = requests.get(url,params=params)
    print(address)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None
    else:
        return None, None

# Iterate through the rows and fill missing lat/lon
for idx, row in summary_df.iterrows():
    if pd.isnull(row['Location Latitude']) or pd.isnull(row['Location Longitude']):
        lat, lon = fix(row['Location Address'])
        summary_df.at[idx, 'Location Latitude'] = lat
        summary_df.at[idx, 'Location Longitude'] = lon

# Save the updated data to a new CSV file
summary_df.to_csv('../data/raw/properties_stats.csv', index=False)
