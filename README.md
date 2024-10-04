# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`.

1. Run `scrape_domain.py` to scrape rental property data from https://www.domain.com.au/.

## Processing External Datasets
1. `notebooks/ext_download.ipynb` downloads external datasets into `data/landing`.
2. `notebooks/ext_preprocess.ipynb` performs column renaming and basic data type conversions on landing data and saves output into `data/raw`.
3. `notebooks/ext_curate.ipynb` filters relevant raw data and combines datasets ready for analysis and modelling. Saves output into `data/curated`.

## Visualisations
- `notebooks/mapping.ipynb` creates various maps of postcode and aggregated property data and saves to `plots`.