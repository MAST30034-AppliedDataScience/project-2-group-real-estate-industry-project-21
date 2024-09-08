
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
    
    bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
    
    # Get the properties... 
    properties = bs_object \
        .find_all("div", {"class": ['property odd clearfix', 'property even clearfix']})

    for property in properties:
        print(property)
    
    try: 
        # looks for the header class to get property name
        property_metadata[property_url]['name'] = bs_object \
            .find() \
            .text
            
        # Beds 
        
        # Baths
        
        # Parking
        
        # (last advertised date and price)
        
        # (lat and long)

    except AttributeError:
        print(f"Issue with {property_url}")
        
        
# output to example json in data/raw/
with open('./data/landing/old_listings_data.json', 'w') as f:
    dump(property_metadata, f)
