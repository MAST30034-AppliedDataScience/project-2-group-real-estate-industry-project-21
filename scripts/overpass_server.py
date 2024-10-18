# Anshan & Zirui
# Debugged with chatgpt
# Library
import pandas as pd
import requests
import folium
import re 

# Build the function to find nearby amenities for properties
def find_nearby_locations(lat, lon, location_type):
    tags = {
        "schools": '["amenity"="school"]',
        "parks": '["leisure"="park"]',
        "supermarkets": '["shop"="supermarket"]',
        "shopping_districts": '["shop"="mall"]',
        "train_stations": '["railway"="station"]',
        "hospitals": '["amenity"="hospital"]'
    }
    
    query = f"""
    [out:json];
    (
      node{tags[location_type]}(around:1000,{lat},{lon});
      way{tags[location_type]}(around:1000,{lat},{lon});
      relation{tags[location_type]}(around:1000,{lat},{lon});
    );
    out body;
    """
    response = requests.get('http://localhost/api/interpreter', params={'data': query})
    data = response.json()
    
    return data['elements']

# Build the function to ensure locations are valid

def process_locations(locations, address):
    
    pattern = r",\s*([A-Za-z\s]+)\s*VIC\s*(\d{4})"
    match = re.search(pattern, address)
    
    if match:
        suburb = match.group(1).strip()  # Suburb (e.g., Coburg)
        postcode = match.group(2).strip()  # Postcode (e.g., 3058)
    
    # Dictionary to store valid locations
    valid_locations = []
    
    for loc in locations:
        
        if 'tags' in loc:
            name = loc['tags'].get('name')
            location_lat = loc.get('lat')
            location_lon = loc.get('lon')

            # Get the address information from tags if available
            
            street_number = loc['tags'].get('addr:housenumber')
            street = loc['tags'].get('addr:street')
            postcode = loc['tags'].get('addr:postcode', postcode)
            suburb = loc['tags'].get('addr:suburb', suburb)
            # Construct the address
            address = f"{street_number} {street}, {suburb}, {postcode}" if street_number and street else None
            
            # Filter locations with either coordinates or address
            if (location_lat and location_lon) or address:
                valid_locations.append({
                    'name': name or "Unnamed Location",
                    'lat': location_lat,
                    'lon': location_lon,
                    'address': address
                })
    
    return valid_locations



# Read the CSV file and save it as a data frame
df = pd.read_csv('../data/landing/properties_and_coordinates.csv')

# Extract postcodes and subrub names
df.insert(0, 'Postcodes', df['Address'].apply(lambda x: x.split('VIC')[-1].strip()))

summary_list = []

#Build the filters of amenitities 
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
            locations = find_nearby_locations(lat, lon, location_type)

            if locations:
                valid_locations = process_locations(locations, address)

                summary[location_type] = {
                    'count': len(locations),  
                    'locations': valid_locations  
                }
    except UnboundLocalError as e:
        print(f"Error processing {address}: {e}")
        continue  # Skip to the next iteration if there's an error

    # Add CBD and its summary as an indivisual amentity for every property
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


    # Add the summary of found nearby amentities for every property 
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

    
summary_df.to_csv('../data/raw/properties_stats_unfixed.csv', index=False)