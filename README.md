# Real Estate Consulting Project
Authors: Anshan Arnott-Tan, Jenny Mai, Vivian To, Zirui Rao

## Project Overview
This project focuses on analyzing real estate data to provide insights and recommendations for property rentals. The analysis includes data scraping, preprocessing, exploratory data analysis (EDA), and visualization. The project also integrates external datasets to enhance the analysis.

## Research Goal
The primary goal of this project is to analyze rental property data and develop insights that can assist in making informed decisions regarding property rentals.

## Project Structure

### Data Scraping
1. **Download Postcode Dataset**
   - 1.Download the complete dataset of Australian postcodes_suburb “australian_postcodes.csv” into  `data/landing` from https://github.com/matthewproctor/australianpostcodesb
   - 2.Run `postcodes_suburbs.py`:Filter the dataset for the unique set of postcode_suburb name for Metro Melbourne Areas.based on the Victoria State Government tourism guidance(https://www.tourismnortheast.com.au/wp-content/uploads/sites/54/Metro-Melb-Postcodes-Factsheet.pdf),saving the output into `data/raw`.

2. **Scrape Domain Links**
   - Run `scrape_domain_links.py` to scrape the links of all rental properties from https://www.domain.com.au.

3. **Scrape Domain Properties**
   - Run `scrape_domain_properties.py` to scrape the metadata of the properties obtained from `scrape_domain_links.py`.

### Data Preprocessing
1. **Preprocess Domain Data**
   - Run `notebooks/preprocess_domain.ipynb`: Handles the initial preprocessing of Domain data.

2. **Processing External Datasets**
   - Run `notebooks/ext_download.ipynb`: Downloads external datasets into `data/landing`.
   - Run `notebooks/ext_preprocess.ipynb`: Performs column renaming and basic data type conversions on landing data, saving the output into `data/raw`.
   - Run `notebooks/ext_curate.ipynb`: Filters relevant raw data and combines datasets for analysis and modeling, saving the output into `data/curated`.
   - Run `properties_and_coodinates.py`: Get the coordinates for every property we scrapped,saving the output into `data/landing`.
   - Run `overpass_server.py`: Get Coordinates for Properties Amenities using Overpass local server,saving the output into `data/raw`.
   - Run `“nominatim_server.py`:Fix missing coordinates for nearby amenities using Nominatim local server,saving the output into `data/raw`.
   - Run `openrouteservice_server.py`:Calculate Counts, Distance,Travel Time between amenities and properties and get the average of those in surbubs using Openrouteservice local server,saving the outputs into `data/raw`.


Calculate Counts, Distance,Travel Time Using Openrouteservice Local Server
1.Run the “openrouteservice_server.py” with “properties_stats.csv”,
The outputs are “properties_stats_completed.csv” and “suburbs_stats.csv” to get total counts, distance, travel time between every property and its amenities and those of average in every suburb.
Note:Previously missing unfindable coordinates cause the calculation errors for some properties, that are handled by calculating the average within their suburbs.


### Exploratory Data Analysis (EDA) and Visualization
1. **EDA and Analysis**
   - Run `notebooks/analysis.ipynb`: Performs exploratory data analysis on the cleaned dataset.

2. **Mapping and Visualization**
   - Run `notebooks/mapping.ipynb`: Creates various maps of postcode and aggregated property data, saving the results to `plots`.

### Modeling
1. **Model Development**
   - Run `notebooks/modelling.ipynb`: Develops and evaluates models for property rental analysis.

## Directories
- **notebooks/**: Contains all Jupyter notebooks for data preprocessing, EDA, and modeling.
- **plots/**: Contains all the plots generated during the EDA and modeling phases.
- **models/**: Contains all models fitted.
- **data/**: Contains all datasets used in the project.

## Requirements
Ensure you have all necessary Python packages installed by using the `requirements.txt` file provided in the root directory.

## Running the Project
To replicate the analysis and run the models, please follow the steps below in the order specified:

### Data Scraping
1. Run `postcodes_suburbs.py`.
2. Run `scrape_domain_links.py`.
3. Run `scrape_domain_properties.py`.

### Data Preprocessing
1. Run `notebooks/preprocess_domain.ipynb`.
2. Run `properties_and_coodinates.py`.
3. Run `overpass_server.py`.
4. Run `“nominatim_server.py`.
5. Run `openrouteservice_server.py`.
6. Run `notebooks/ext_download.ipynb`.
7. Run `notebooks/ext_preprocess.ipynb`.
8. Run `notebooks/ext_curate.ipynb`.

### Exploratory Data Analysis (EDA) and Visualization
1. Run `notebooks/analysis.ipynb`.
2. Run `notebooks/mapping.ipynb`.

### Modeling
1. Run `notebooks/modelling.ipynb`.
