"""
A basic web scraping script to get the links of properties in Melbourne's metropolitian area

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
file_path = './data/raw/Mel_Metro_Postcodes.csv'

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

for suburb in list_of_suburbs[1:]: 
    
    suburb_name = suburb[1].lower().replace(" ", "-")
    postcode = suburb[0]

    # generate list of urls to visit
    page = 1
    while True:

        try: 
            # Try the request... if it works amazo... 
            url = BASE_URL + f"/rent/?ssubs=0&sort=suburb-asc&postcode={postcode}&page={page}"
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

# The number of properties scraped... 
print(f"The number of properties scraped is {len(url_links)}\n")

# Save the links to a file 
with open('./data/landing/property_urls.txt', 'w') as file:
    for url in url_links:
        file.write(url + '\n')
