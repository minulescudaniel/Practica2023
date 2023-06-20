import requests
import re
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# Set your API key and search engine ID
API_KEY = 'AIzaSyCr6Yvpz6CNLYhZHWn2vrd7QE3GO--ao9o'
SEARCH_ENGINE_ID = '802c9ced402b44931'

# Create a service object for interacting with the API
service = build('customsearch', 'v1', developerKey=API_KEY)

user_input = input("Enter your search query: ")
print("Searching...")

# Make a search request with country restriction
res = service.cse().list(q=user_input, cx=SEARCH_ENGINE_ID, cr='countryRO').execute()

# Extract and print the URLs and information from the search results
counter = 0
for result in res['items']:
    url = result['link']
    print("URL:", url)

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the price if available
    price = None
    # Modify the code below to extract the price based on the structure of the specific webpage
    # For example, if the price is in a span element with class "price", you can use:
    price_element = soup.find('span', class_='price')
    if price_element:
        price = price_element.text
        print("Price:", price)

    # Extract the product information if available
    product_info = None
    # Modify the code below to extract the product information based on the structure of the specific webpage
    possible_element_names = ["h1", "h1 page-title", "div page-title","product-highlights"]
    for element_name in possible_element_names:
        info_element = soup.find(element_name)
        if info_element:
            product_info = info_element.text.strip()
            break

    if product_info:
        print("Product Information:", product_info)

    # Print a newline for separation
    print()

    counter += 1
    if counter == 5:
        break
