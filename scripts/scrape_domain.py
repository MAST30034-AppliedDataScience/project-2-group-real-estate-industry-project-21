"""
A very simple, naive, and basic web scraping script. This will not
work completely and is only applicable to domain.com.

Feel free to use this as a source of inspiration, it is by no means production code.

Edited and Debugged with ChatGPT - AAT

"""
# built-in imports
import re
import csv
from json import dump
from tqdm import tqdm

from collections import defaultdict
from urllib.error import URLError, HTTPError

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request 

# Replace 'your_file.csv' with the path to your actual CSV file
file_path = './data/landing/final.csv'

# Initialize an empty list to store the rows
list_of_suburbs = []

# Open and read the CSV file
with open(file_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        list_of_suburbs.append(row)
        
# constants
BASE_URL = "https://www.domain.com.au"
# N_PAGES = range(1, 5) # update this to your liking

# begin code
url_links = []
property_metadata = defaultdict(dict)

for suburb in list_of_suburbs[1:]: 
    
    suburb_name = suburb[0].lower().replace(" ", "-")
    postcode = suburb[1]

    # generate list of urls to visit
    page = 1
    while True:

        try: 
            # Try the request... if it works amazo... 
            url = BASE_URL + f"/rent/{suburb_name}-vic-{postcode}/?sort=suburb-asc&page={page}"
            print(f"Visiting {url}")
            request = urlopen(Request(url, headers={'User-Agent':"PostmanRuntime/7.6.0"}))

        except HTTPError as e:
            print(f"HTTP Error on page {page}")
            break  # Stop the loop when an HTTP error occurs
        except URLError as e:
            print(f"URL Error on page {page}")
            break  # Stop the loop when a URL error occurs
        
        bs_object = BeautifulSoup(request, "lxml")

        # find the unordered list (ul) elements which are the results, then
        # find all href (a) tags that are from the base_url website.
        try: 
            index_links = bs_object \
                .find(
                    "ul",
                    {"data-testid": "results"}
                ) \
                .findAll(
                    "a",
                    href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
                )

            for link in index_links:
                # if its a property address, add it to the list
                if 'address' in link['class']:
                    url_links.append(link['href'])
            
            page += 1 
        
        # if there is an issue with the page, then break out of the loop
        except AttributeError:
            print(f"Issue with {url}") 
            break

# for each url, scrape some metadata
pbar = tqdm(url_links[0:])
success_count, total_count = 0, 0
for property_url in pbar:
    bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
    total_count += 1    
    
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

        property_metadata[property_url]['prop_type'] = bs_object \
            .find("div", {"data-testid": "listing-summary-property-type"}) \
            .text
        
        # Additional features info... 
        add_features = bs_object \
            .find("ul", {"class": "css-4ewd2m"}) \
            .findAll("li", {"data-testid": "listing-details__additional-features-listing"})
        
        property_metadata[property_url]['additional_features'] = [feature.text for feature in add_features]

        success_count += 1
        
    except AttributeError:
        print(f"Issue with {property_url}")

    pbar.set_description(f"{(success_count/total_count * 100):.0f}% successful")

# output to example json in data/raw/
with open('./data/landing/domain_data.json', 'w') as f:
    dump(property_metadata, f)
    
    



