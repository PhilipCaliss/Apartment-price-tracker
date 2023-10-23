from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.hemnet.se/bostader?location_ids%5B%5D=925964&item_types%5B%5D=bostadsratt&page="
headers = {'User-Agent': '*'}
page_num = 1

while True:
    url = BASE_URL + str(page_num)
    response = requests.get(url, headers=headers)
    
    # If the server responds with 404, break out of the loop
    if response.status_code == 404:
        print(f"Reached end at page {page_num}. Server responded with 404.")
        break
    
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select("h2.listing-card__street-address.qa-listing-title")
    
    for title in titles:
        print(f"[Response {response.status_code} - Page {page_num}] {title.text.strip()}")
    
    page_num += 1
