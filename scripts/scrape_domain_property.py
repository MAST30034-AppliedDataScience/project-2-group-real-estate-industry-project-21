"""
This is a scraping code for properties on domain.com.au, it builds on the previous script by going through the links of the properties we scraped before 

Edited and Debugged with ChatGPT - AAT

"""
# built-in imports
import re
import csv
from json import dump
from tqdm import tqdm
import time

from collections import defaultdict
from urllib.error import HTTPError, URLError

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request 

# In case of timeout errors
max_retries = 3
delay = 5

property_metadata = defaultdict(dict)

with open('./data/landing/property_urls.txt', 'r') as file:
    url_links = [line.strip() for line in file]

# for each url, scrape some metadata
pbar = tqdm(url_links[1:])
for property_url in pbar:
    
    for attempt in range(max_retries):
        try: 
            bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
            # since sucessful don't need to continue with this... 
            break
            
        # in case of HTTP error... 
        except HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason} on property {property_url}")
            break
        
        except URLError as e:
            if isinstance(e.reason, TimeoutError):
                print(f"Timeout error. Retrying in {delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)  # Wait before retrying
            else:
                print(f"URL Error: {e.reason} on page {property_url}")
                break  # For non-timeout errors, stop retrying and break out
            
        # If you exhaust the retries, then move on to the next property... 
    else: 
        print(f"Max retries reached for page {property_url}. Moving to the next property.")
        continue

    try: 
        # looks for the header class to get property name
        property_metadata[property_url]['name'] = bs_object \
            .find("h1", {"class": "css-164r41r"}) \
            .text

        # looks for the div containing a summary title for cost
        property_metadata[property_url]['cost_text'] = bs_object \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text

        # get rooms and parking
        rooms = bs_object \
                .find("div", {"data-testid": "property-features"}) \
                .findAll("span", {"data-testid": "property-features-text-container"})

        # rooms
        property_metadata[property_url]['rooms'] = [
            re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Bed' in feature.text or 'Bath' in feature.text
        ]
        # parking
        property_metadata[property_url]['parking'] = [
            re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Parking' in feature.text
        ]

        # Property description
        prop_desc = bs_object \
            .find("div", {"data-testid": "listing-details__description"}) \
            .findAll("p")
        
        property_metadata[property_url]['description'] = "\n".join([p.text for p in prop_desc])

        # Property Type 
        property_metadata[property_url]['prop_type'] = bs_object \
            .find("div", {"data-testid": "listing-summary-property-type"}) \
            .text
        
        # Additional features info... 
        add_features = bs_object \
            .find("ul", {"class": "css-4ewd2m"}) \
            .findAll("li", {"data-testid": "listing-details__additional-features-listing"})
        
        property_metadata[property_url]['additional_features'] = [feature.text for feature in add_features]

    except AttributeError:
        print(f"Issue with {property_url}")

# output to example json in data/raw/
with open('./data/landing/domain_data.json', 'w') as f:
    dump(property_metadata, f)
    
    
print(f"The number of properties that were scraped is {len(property_metadata)}")


