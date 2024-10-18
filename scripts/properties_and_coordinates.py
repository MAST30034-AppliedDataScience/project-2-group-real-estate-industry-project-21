#Debugged with chatgpt
import json
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# Load the JSON file
file_path = '../data/landing/domain_data.json'

with open(file_path, 'r') as f:
    data = json.load(f)

# Create a DataFrame directly from the JSON data
urls_df = pd.DataFrame({
    'Address': [details.get('name') for details in data.values()],
    'URLS': list(data.keys()),
})


# Initialize 'Latitude' and 'Longitude' columns
urls_df['Latitude'] = ''
urls_df['Longitude'] = ''

# Iterate through each URL and parse the webpage for coordinates
for index, row in urls_df.iterrows():
    url = row['URLS']  # The URLs are stored in the 'URLS' column

    try:
        # Set up headers to mimic a real browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        # Parse the webpage with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the script containing the coordinates
        scripts = soup.find_all('script', text=re.compile(r'"latitude"'))

        found = False
        for script in scripts:
            script_text = script.string
            if script_text:
                # Use regex to find latitude and longitude
                coordinates = re.findall(
                    r'"latitude"\s*:\s*([-\d.]+),\s*"longitude"\s*:\s*([-\d.]+)', script_text)
                if coordinates:
                    latitude, longitude = coordinates[0]
                    urls_df.at[index, 'Latitude'] = latitude
                    urls_df.at[index, 'Longitude'] = longitude
                    found = True
                    break  # Exit the loop after finding the coordinates

        if not found:
            urls_df.at[index, 'Latitude'] = 'Not Found'
            urls_df.at[index, 'Longitude'] = 'Not Found'

    except Exception as e:
        print(f"Error fetching coordinates for {url}: {e}")
        urls_df.at[index, 'Latitude'] = 'Error'
        urls_df.at[index, 'Longitude'] = 'Error'

    # Add a short delay between requests to avoid overwhelming the server
    time.sleep(5)

# Save the updated DataFrame with coordinates to a new CSV file
urls_df.to_csv('../data/landing/properties_and_coordinates.csv', index=False)
print('done')