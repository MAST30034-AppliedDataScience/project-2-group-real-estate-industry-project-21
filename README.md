# Generic Real Estate Consulting Project

1. Download the postcode dataset from landing folder first [Download the dataset](data/landing/Mel_Metro_Postcodes.csv.csv)
2. Run `scrape_domain_links.py` to scrape the links of all the rental properties we will consider from https://www.domain.com.au/.
3. Run `scrape_domain_properties.py` to scrape the metadata of the properties we scraped from `scrape_domain_links.py`

## Processing External Datasets
1. `notebooks/ext_download.ipynb` downloads external datasets into `data/landing`.
2. `notebooks/ext_preprocess.ipynb` performs column renaming and basic data type conversions on landing data and saves output into `data/raw`.
3. `notebooks/ext_curate.ipynb` filters relevant raw data and combines datasets ready for analysis and modelling. Saves output into `data/curated`.

## Visualisations
- `notebooks/mapping.ipynb` creates various maps of postcode and aggregated property data and saves to `plots`.