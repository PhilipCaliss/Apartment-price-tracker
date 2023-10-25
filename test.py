from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.hemnet.se/bostader?location_ids%5B%5D=925964&item_types%5B%5D=bostadsratt&page="
headers = {'User-Agent': '*'}
page_num = 1
all_listings = []

while True:
    url = BASE_URL + str(page_num)
    response = requests.get(url, headers=headers)

    # If the server responds with 404, break out of the loop
    if response.status_code == 404:
        print(f"Reached end at page {page_num}. Server responded with 404.")
        break
    
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.select("div.listing-card__information-container")

    print(f"Page {page_num} detected listings: {len(listings)}")

    for listing in listings:
        title_tag = listing.select_one("h2.listing-card__street-address.qa-listing-title")
        
        listing_id_tag = listing.parent.parent.get('id') if listing.parent.parent else None  # Fetch id from the grandparent
        
        if title_tag and listing_id_tag:
            listing_data = {
                'title': title_tag.text.strip(),
                'listing_id': listing_id_tag.replace('listing_', '')  # Remove the 'listing_' prefix
            }
            all_listings.append(listing_data)
    
    page_num += 1

print(all_listings)
