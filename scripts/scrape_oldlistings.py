
"""
A Web scraping script for the old listings website 

Currently just for one page... (being blocked from Website)

Edited and Debugged with ChatGPT - AAT

"""

# built-in imports
import re
from json import dump
from tqdm import tqdm

from collections import defaultdict
from urllib.error import URLError, HTTPError

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request 

# Want to get address, bed, bath and parking, (last advertised date and price), (lat and long) into a dictionary... 

property_metadata = defaultdict(dict)

list_of_urls = ["https://www.oldlistings.com.au/real-estate/VIC/Heidelberg/3084/rent/1"]

for property_url in list_of_urls:
    
    bs_object = BeautifulSoup(urlopen(Request(property_url, 
                                              headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"})), "lxml")
    # Get the properties... 
    properties = bs_object \
        .find_all("div", {"class": ['property odd clearfix', 'property even clearfix']})

    for property in properties:

        try: 
            # looks for the header class to get property name
            property_name = property \
                .find("h2", {'class': 'address'}) \
                .text \
                .strip()

            # Beds 
            property_metadata[property_name]['bed'] = property \
                .find("p", {'class': 'property-meta bed'}) \
                .text \
                .strip()
            
            # Baths
            property_metadata[property_name]['baths'] = property \
                .find("p", {'class': 'property-meta bath'}) \
                .text \
                .strip()
            
            # Parking
            property_metadata[property_name]['parking'] = property \
                .find("p", {'class': 'property-meta car'}) \
                .text \
                .strip()
            
            # (last advertised date and price)
            property_metadata[property_name]['price'] = property \
                .find("section", {"class", "grid-35 tablet-grid-35 price"}).text \
                .strip()

            # Historical prices 
            property_metadata[property_name]['history'] = property \
                .find("section", {"class", "grid-100 historical-price"}).text \
                .strip()

        except AttributeError:
            print(f"Issue with {property_url}")
        
        
# output to example json in data/raw/
with open('./data/landing/old_listings_data.json', 'w', encoding = 'utf-8') as f:
    dump(property_metadata, f, ensure_ascii=False, separators=(',', ':'))



# Want to have the dictionary with the address as the key, and the other info as everything else... 