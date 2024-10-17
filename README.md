# Real Estate Consulting Project
Authors: Anshan Arnott-Tan, Jenny Mai, Vivian To, Zirui Rao

## Project Overview
This project focuses on analyzing real estate data to provide insights and recommendations for property rentals. The analysis includes data scraping, preprocessing, exploratory data analysis (EDA), and visualization. The project also integrates external datasets to enhance the analysis.

## Research Goal
The primary goal of this project is to analyze rental property data and develop insights that can assist in making informed decisions regarding property rentals.

## Project Structure

### Data Scraping
1. **Download Postcode Dataset**
   - Download the postcode dataset from the landing folder: [Download the dataset](data/landing/Mel_Metro_Postcodes.csv.csv).

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
1. Run `scrape_domain_links.py`.
2. Run `scrape_domain_properties.py`.

### Data Preprocessing
1. Run `notebooks/preprocess_domain.ipynb`.
2. Run `notebooks/ext_download.ipynb`.
3. Run `notebooks/ext_preprocess.ipynb`.
4. Run `notebooks/ext_curate.ipynb`.

### Exploratory Data Analysis (EDA) and Visualization
1. Run `notebooks/analysis.ipynb`.
2. Run `notebooks/mapping.ipynb`.

### Modeling
1. Run `notebooks/modelling.ipynb`.