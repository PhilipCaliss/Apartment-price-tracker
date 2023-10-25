from bs4 import BeautifulSoup
import requests
import pandas as pd



BASE_URL = "https://www.hemnet.se/bostader?location_ids%5B%5D=925964&item_types%5B%5D=bostadsratt&page="
LISTING_URL = "https://www.hemnet.se/bostad/"
headers = {"User-Agent": "*"}


def clean_price(price):
    return price.replace("\xa0", " ")

def get_page_soup(page_num):
    response = requests.get(f"{BASE_URL}{page_num}", headers=headers)
    if response.status_code == 404:
        return None
    return BeautifulSoup(response.text, "html.parser")

def get_broker_info(listing_id):
    url = f"{LISTING_URL}{listing_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, "html.parser")

def get_listing_details(listing):
    def get_text(selector):
        element = listing.select_one(selector)
        return element.text.strip() if element else None

    listing_id_attr = listing.attrs.get("data-tracking-data")
    listing_id = eval(listing_id_attr).get("listingId") if listing_id_attr else None

    return {
        "Title": get_text("h2.listing-card__street-address.qa-listing-title"),
        "Listed Price": clean_price(get_text("div.listing-card__attributes-row div.listing-card__attribute--primary")),
        "Apartment Size": get_text("div.listing-card__attributes-row > div:nth-child(2)"),
        "Number of Rooms": get_text("div.listing-card__attributes-row > div:nth-child(3)"),
        "Monthly Price": clean_price(get_text("div.listing-card__attributes-row + div.listing-card__attributes-row div.listing-card__attribute--fee"))
    }

def get_broker_company_name(listing_id):
    broker_info = get_broker_info(listing_id)
    if broker_info is None:
        return None

    broker_tag = broker_info.select_one("div.listing-card__broker > div.listing-card__broker-info > a")
    if broker_tag and 'data-broker-agency-name' in broker_tag.attrs:
        print(f"Processing listing ID {listing_id}")
        return broker_tag['data-broker-agency-name']
    return None

def main():
    page_num = 1
    all_apartments_data = {}

    while True:
        soup = get_page_soup(page_num)
        if soup is None:
            print("Status_code 404 - No more pages to scrape.")
            break

        print(f"Scraping page {page_num}...")
        listings_elements = soup.select("li.normal-results__hit")
        
        for listing in listings_elements:
            listing_details = get_listing_details(listing)
            listing_id = eval(listing.attrs.get("data-tracking-data", {})).get("listingId", None)
            all_apartments_data[listing_id] = listing_details

        page_num += 1

    listings_df = pd.DataFrame.from_dict(all_apartments_data, orient="index")
    
    print('grabbing broker company names')
    listings_df['Broker Name'] = listings_df.index.map(lambda x: get_broker_company_name(x))
    print(listings_df)
    return listings_df

if __name__ == "__main__":
   x = main()
   x.to_excel('hemnet.xlsx')