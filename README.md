# Real Estate Consulting Project
Authors: Anshan Arnott-Tan, Jenny Mai, Vivian To, Zirui Rao

## Project Overview
This project focuses on analyzing real estate data to provide insights and recommendations for property rentals. The analysis includes data scraping, preprocessing, exploratory data analysis (EDA), and visualization. The project also integrates external datasets to enhance the analysis.

## Research Goal
The primary goal of this project is to analyze rental property data and develop insights that can assist in making informed decisions regarding property rentals.

## Project Structure

### Data Collection
1. **Download Postcode Dataset**
   - Download the complete dataset of Australian postcodes `australian_postcodes.csv` into `data/landing` from [here](https://github.com/matthewproctor/australianpostcodes).
   - Run `postcodes_suburbs.py`: filters the dataset for the unique set of postcode/suburb names for metropolitan Melbourne, saving the output into `data/raw`. Based on the [Victoria State Government tourism guide](https://www.tourismnortheast.com.au/wp-content/uploads/sites/54/Metro-Melb-Postcodes-Factsheet.pdf).

2. **Scrape Domain Links**
   - Run `scrape_domain_links.py`: scrapes the links of all rental properties from [Domain](https://www.domain.com.au).

3. **Scrape Domain Properties**
   - Run `scrape_domain_properties.py`: scrapes the metadata of the properties obtained from `scrape_domain_links.py`.

4. **Download External Datasets**
   - Run `notebooks/ext_download.ipynb`: downloads external datasets into `data/landing`.

### Data Preprocessing and Feature Engineering
1. **Preprocess Domain Data**
   - Run `notebooks/preprocess_domain.ipynb`: handles the initial preprocessing of Domain data.

2. **Preprocess External Datasets**
   - Run `notebooks/ext_preprocess.ipynb`: performs column renaming and basic data type conversions on landing data, saving the output into `data/raw`.

   - Run `notebooks/ext_curate.ipynb`: filters relevant raw data and combines datasets for analysis and modeling, saving the output into `data/curated`.

3. **Engineer Domain Data**
   - Run `properties_and_coodinates.py`: gets the coordinates for every property previously scraped, saving the output into `data/landing`.

   - Run `overpass_server.py`: gets coordinates for properties' amenities using Overpass local server,saving the output into `data/raw`.

   - Run `nominatim_server.py`: fixes missing coordinates for nearby amenities using Nominatim local server, saving the output into `data/raw`.

   - Run `openrouteservice_server.py`: calculates counts, distance, and travel time between amenities and properties and gets the average of those in surbubs using Openrouteservice local server, saving the outputs into `data/raw`.

### Exploratory Data Analysis (EDA) and Visualization
1. **EDA and Analysis**
   - Run `notebooks/analysis.ipynb`: performs exploratory data analysis on the cleaned dataset.

2. **Mapping and Visualization**
   - Run `notebooks/mapping.ipynb`: creates various maps of postcode and aggregated property data, saving the results to `plots`.

### Modeling
1. **Model Development**
   - Run `notebooks/modelling.ipynb`: develops and evaluates models for property rental analysis.

## Directories
- **data/**: contains all datasets used in the project.
- **plots/**: contains all the plots generated during the EDA and modeling phases.
- **models/**: contains all models fitted.
- **notebooks/**: contains all Jupyter notebooks for data preprocessing, EDA, and modeling.
- **scripts/**: contains all Python scripts used in the project.

## Requirements
Ensure you have all necessary Python packages installed by using the `requirements.txt` file provided in the root directory.

## Running the Project
To replicate the analysis and run the models, please follow the steps below in the order specified:

### Data Collectinng
1. Download `australian_postcodes.csv` ([source](https://github.com/matthewproctor/australianpostcodes)).
2. Run `postcodes_suburbs.py`.
3. Run `scrape_domain_links.py`.
4. Run `scrape_domain_properties.py`.
5. Run `notebooks/ext_download.ipynb`.

### Data Preprocessing and Feature Engineering
1. Run `notebooks/preprocess_domain.ipynb`.
2. Run `notebooks/ext_preprocess.ipynb`.
3. Run `notebooks/ext_curate.ipynb`.
2. Run `properties_and_coodinates.py`.
3. Run `overpass_server.py`.
4. Run `nominatim_server.py`.
5. Run `openrouteservice_server.py`.

### Exploratory Data Analysis (EDA) and Visualization
1. Run `notebooks/analysis.ipynb`.
2. Run `notebooks/mapping.ipynb`.

### Modeling
1. Run `notebooks/modelling.ipynb`.
