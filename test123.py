from bs4 import BeautifulSoup
import requests
import json

BASE_URL = "https://www.hemnet.se/bostader?location_ids%5B%5D=925964&item_types%5B%5D=bostadsratt&page="
headers = {'User-Agent': '*'}
page_num = 1

response = requests.get(BASE_URL + str(page_num), headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

listings = soup.select("li.normal-results__hit")

# Only inspecting the first listing for debugging
listing = listings[0]

title_tag = listing.select_one("h2.listing-card__street-address.qa-listing-title")

# Extracting the listing ID from the JSON attribute
listing_info_json = listing.attrs.get("data-gtm-item-info", "{}")
listing_info = json.loads(listing_info_json)
listing_id = listing_info.get("id")

print(f"Title from title_tag: {title_tag.text.strip() if title_tag else 'Not Found'}")
print(f"ID from listing_id: {listing_id if listing_id else 'Not Found'}")
