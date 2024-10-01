import time
import pandas as pd
from json.decoder import JSONDecodeError

summary_list = []

# Build the filters of amenities
location_types = ["schools", "parks", "supermarkets", "shopping_districts", "train_stations", "hospitals"]

# Create an empty DataFrame with summary columns
summary_df = pd.DataFrame(columns=['Postcodes', 'Address', 'URLS', 'Latitude', 'Longitude', 'Location Type', 'Count', 'Location Name', 'Location Address', 'Location Latitude', 'Location Longitude'])

for index, row in df.iterrows():
    postcodes = row['Postcodes']
    address = row['Address']
    urls = row['URLS']
    lat = row['Latitude']
    lon = row['Longitude']

    summary = {}

    try:
        for location_type in location_types:
            try:
                locations = find_nearby_locations(lat, lon, location_type)
                
                # Check if locations are found and process them
                if locations:
                    valid_locations = process_locations(locations, address)
                    summary[location_type] = {
                        'count': len(locations),  
                        'locations': valid_locations  
                    }
                else:
                    print(f"No locations found for {location_type} at {address}")
            
            # Catch potential JSON errors or other exceptions within find_nearby_locations
            except JSONDecodeError as e:
                print(f"JSON decoding error for {address} and location type {location_type}: {e}")
                continue

            # Add a delay of 1 second after processing each location_type
            time.sleep(1)

    except UnboundLocalError as e:
        print(f"Error processing {address}: {e}")
        continue  # Skip to the next iteration if there's an error

    # Add CBD and its summary as an individual amenity for every property
    summary_df = pd.concat([summary_df, pd.DataFrame([{
        'Postcodes': postcodes,
        'Address': address,
        'URLS': urls,
        'Latitude': lat,
        'Longitude': lon,
        'Location Type': 'CBD',  # Example row
        'Count': '1',
        'Location Name': 'CBD',
        'Location Address': '',
        'Location Latitude': '-37.8124',
        'Location Longitude': '144.9623'
    }])], ignore_index=True)

    # Add the summary of found nearby amenities for every property 
    for location_type, counts in summary.items():
        count = counts['count']
        for loc in counts['locations']:
            summary_df = pd.concat([summary_df, pd.DataFrame([{
                'Postcodes': postcodes,
                'Address': address,
                'URLS': urls,
                'Latitude': lat,
                'Longitude': lon,
                'Location Type': location_type,
                'Count': count,
                'Location Name': loc['name'],
                'Location Address': loc['address'],
                'Location Latitude': loc['lat'],
                'Location Longitude': loc['lon']
            }])], ignore_index=True)

    # Add a delay of 1 second between processing each property
    time.sleep(1)