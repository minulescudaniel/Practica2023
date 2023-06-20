import requests
import re
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


API_KEY = 'AIzaSyCr6Yvpz6CNLYhZHWn2vrd7QE3GO--ao9o'
SEARCH_ENGINE_ID = '802c9ced402b44931'


service = build('customsearch', 'v1', developerKey=API_KEY)

user_input = input("Enter your search query: ")
print("Searching...")


res = service.cse().list(q=user_input, cx=SEARCH_ENGINE_ID, cr='countryRO').execute()


counter = 0
for result in res['items']:
    url = result['link']
    print("URL:", url)

   
    response = requests.get(url)

   
    soup = BeautifulSoup(response.text, 'html.parser')

    price = None
   
    price_element = soup.find('span', class_='price')
    if price_element:
        price = price_element.text
        print("Price:", price)

    
    product_info = None
    
    possible_element_names = ["h1", "h1 page-title", "div page-title","product-highlights"]
    for element_name in possible_element_names:
        info_element = soup.find(element_name)
        if info_element:
            product_info = info_element.text.strip()
            break

    if product_info:
        print("Product Information:", product_info)

   
    print()

    counter += 1
    if counter == 5:
        break
