"""
A very simple, naive, and basic web scraping script. This will not
work completely and is only applicable to domain.com.

Feel free to use this as a source of inspiration, it is by no means production code.

Edited and Debugged with ChatGPT

"""
# built-in imports
import re
from json import dump
from tqdm import tqdm

from collections import defaultdict
import urllib.request

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# constants
BASE_URL = "https://www.domain.com.au"
N_PAGES = range(1, 5) # update this to your liking

# begin code
url_links = []
property_metadata = defaultdict(dict)

# generate list of urls to visit
for page in N_PAGES:
    url = BASE_URL + f"/rent/melbourne-region-vic/?sort=price-desc&page={page}"
    print(f"Visiting {url}")
    bs_object = BeautifulSoup(urlopen(Request(url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")

    # find the unordered list (ul) elements which are the results, then
    # find all href (a) tags that are from the base_url website.
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

# for each url, scrape some basic metadata
pbar = tqdm(url_links[1:])
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
        
        property_metadata[property_url]['prop_type'] = bs_object \
            .find("div", {"data-testid": "listing-summary-property-type"}) \
            .text

        # get rooms and parking
        rooms = bs_object \
                .find("div", {"data-testid": "property-features"}) \
                .findAll("span", {"data-testid": "property-features-text-container"})

        # Additional features info... 
        add_features = bs_object \
            .find("div", {"data-testid": "listing-details__additional-features"}) \
            .findAll("li", {"data-testid": "listing-details__additional-features-listing"})
        property_metadata[property_url]['additional_features'] = [feature.text for feature in add_features]

        # Property description
        prop_desc = bs_object \
            .find("div", {"data-testid": "listing-details__description"}) \
            .findAll("p")
        property_metadata[property_url]['description'] = "\n".join([p.text for p in prop_desc])

        # Close schools... (For Government...) + Their distance from the house... 
        # (+ other features, eg priv, junior, high, coed etc)

        """
        There is an issue here... 
        just scraping the government schools rather than government and independent schools 
        """

        schools_info = []

        schools = bs_object \
            .findAll("div", {"data-testid": "fe-co-school-catchment-content"}) 

        for school_types in schools:
            school_types = school_types.findAll("li", {"data-testid": "fe-co-school-catchment-school"})

            for school in school_types:
                schools_info.append(school.text)
        
        property_metadata[property_url]['school_info'] = schools_info
        
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

        success_count += 1
        
    except AttributeError:
        print(f"Issue with {property_url}")

    pbar.set_description(f"{(success_count/total_count * 100):.0f}% successful")

# output to example json in data/raw/
with open('./data/landing/example.json', 'w') as f:
    dump(property_metadata, f)

