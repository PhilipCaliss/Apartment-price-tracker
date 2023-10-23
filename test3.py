from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.hemnet.se/bostader?location_ids%5B%5D=925964&item_types%5B%5D=bostadsratt&page="
headers = {'User-Agent': '*'} # This is to avoid getting blocked by the server, check www.hemnet.se/robots.txt
page_num = 1



response = requests.get(BASE_URL + str(page_num), headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
listings = soup.select("li.normal-results__hit")

# Only inspecting the first listing for debugging
listing = listings[0]

# Extracting the details
title_tag = listing.select_one("h2.listing-card__street-address.qa-listing-title")
listing_id_attr = listing.attrs.get("data-tracking-data")
if listing_id_attr:
    listing_id = eval(listing_id_attr).get("listingId")
else:
    listing_id = None

def clean_price(price):
    return price.replace('\xa0', ' ')


listed_price = clean_price(listing.select_one("div.listing-card__attributes-row div.listing-card__attribute--primary").text.strip()) if listing.select_one("div.listing-card__attributes-row div.listing-card__attribute--primary") else None
apartment_size = listing.select_one("div.listing-card__attributes-row > div:nth-child(2)").text.strip() if listing.select_one("div.listing-card__attributes-row > div:nth-child(2)") else None
num_rooms = listing.select_one("div.listing-card__attributes-row > div:nth-child(3)").text.strip() if listing.select_one("div.listing-card__attributes-row > div:nth-child(3)") else None
monthly_price = clean_price(listing.select_one("div.listing-card__attributes-row + div.listing-card__attributes-row div.listing-card__attribute--fee").text.strip()) if listing.select_one("div.listing-card__attributes-row + div.listing-card__attributes-row div.listing-card__attribute--fee") else None

# Creating the dictionary
apartment_data = {
    listing_id: {
        "Title": title_tag.text.strip() if title_tag else 'Not Found',
        "Listed Price": listed_price,
        "Apartment Size": apartment_size,
        "Number of Rooms": num_rooms,
        "Monthly Price": monthly_price
    }
}

#TODO: Refactor above to iterate through all the results and pages.
#TODO: To fetch brokers, go to www.hemnet.se/bostad/{listing_id} and extract the broker name from the page

print(apartment_data)
