# Anshan & Zirui
# Debugged with chatgpt
# Library
import openrouteservice as ors
import pandas as pd
import folium 
import json
import csv

# load local server api 
client = ors.Client(base_url='http://localhost:8080/ors')


# Open the csv and process for every row of address
with open('../data/raw/properties_stats.csv', mode='r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    rows = list(reader)

    # Add new 'Travel Time (minutes)' and 'Travel Distance (km)' columns to the header
    fieldnames = reader.fieldnames + ['Travel Time (minutes)', 'Travel Distance (km)']
    
    # Create an empty list to store processed rows
    processed_data = []

    for row in rows:
        try:
            # Get coordinates and calculate travel time and distance
            lat1, lon1 = float(row['Latitude']), float(row['Longitude'])
            lat2, lon2 = float(row['Location Latitude']), float(row['Location Longitude'])
            coords = [[lon1, lat1], [lon2, lat2]]

            # Call OpenRouteService API to get route information
            route = client.directions(coordinates=coords, profile='driving-car', format='geojson')
            
            # Extract travel time in minutes and distance in kilometers
            travel_time_minutes = route['features'][0]['properties']['summary']['duration'] / 60
            travel_distance_km = route['features'][0]['properties']['summary']['distance'] / 1000

            # Update the row with travel time and distance
            row['Travel Time (minutes)'] = f"{travel_time_minutes:.2f}"
            row['Travel Distance (km)'] = f"{travel_distance_km:.2f}"

            print(f"Processed travel time and distance for {row['Address']} to {row['Location Name']}: {travel_time_minutes:.2f} minutes, {travel_distance_km:.2f} km")

        except Exception as e:
            print(f"Error processing row {row['Address']} to {row['Location Name']}: {e}")
            row['Travel Time (minutes)'] = 'Error'
            row['Travel Distance (km)'] = 'Error'

        # Add the updated row to the processed data list
        processed_data.append(row)

# Convert the processed data to a DataFrame
df = pd.DataFrame(processed_data)


# Convert 'Travel Time (minutes)' and 'Travel Distance (km)' to numeric, coercing errors to NaN
df['Travel Time (minutes)'] = pd.to_numeric(df['Travel Time (minutes)'], errors='coerce')
df['Travel Distance (km)'] = pd.to_numeric(df['Travel Distance (km)'], errors='coerce')

# Compute the mean travel time and distance for each group (Postcodes and Location Type)
group_means = df.groupby(['Postcodes', 'Location Type'])[['Travel Time (minutes)', 'Travel Distance (km)']].mean()

# Iterate over each row in the dataframe
for index, row in df.iterrows():

    
    # Check if there's an error in 'Travel Time (minutes)' or 'Travel Distance (km)'
    travel_time_error = pd.isna(row['Travel Time (minutes)'])
    travel_distance_error = pd.isna(row['Travel Distance (km)'])

    if travel_time_error or travel_distance_error:
        postcode = row['Postcodes']
        location_type = row['Location Type']
        
        # Get the mean values for the group
        mean_values = group_means.loc[(postcode, location_type)]

        # Replace erroneous values with the mean of the corresponding group
        if travel_time_error:
            df.at[index, 'Travel Time (minutes)'] = mean_values['Travel Time (minutes)']
        if travel_distance_error:
            df.at[index, 'Travel Distance (km)'] = mean_values['Travel Distance (km)']

 # The corrected dataframe for counts/distance/time are saved to a csv file           
df.to_csv('../data/raw/properties_stats_final.csv', index=False)

# Build the dataframe for suburbs average statistics.
df_suburb = df[(df['Travel Distance (km)'] <= 5) | (df['Location Type'] == 'CBD')]


df_suburb['Count'] = pd.to_numeric(df_suburb['Count'], errors='coerce')

# Calculate unique address counts per postcode
address_count_by_postcode = df_suburb.groupby('Postcodes')['Address'].nunique().reset_index()
address_count_by_postcode.columns = ['Postcodes', 'Unique Address Count']

# get the total count, average travel distance, and average travel time
df_suburb_postcodes = df_suburb.groupby(['Postcodes', 'Location Type']).agg(
    Count=('Count', 'sum'),
    Average_Distance=('Travel Distance (km)', 'mean'),
    Average_Time=('Travel Time (minutes)', 'mean')
).reset_index()

# Merge with address count to calculate average count
df_suburb_postcodes  = pd.merge(df_suburb_postcodes , address_count_by_postcode, on='Postcodes')
df_suburb_postcodes ['Average Count'] = df_suburb_postcodes ['Count'] / df_suburb_postcodes ['Unique Address Count']

# Drop unnecessary columns for final output
final_average_data = df_suburb_postcodes [['Postcodes', 'Location Type', 'Count', 'Average Count', 'Average_Distance', 'Average_Time']]

# Save the dataframe to a csv file
final_average_data.to_csv('../data/raw/suburbs_stats.csv',index=False)