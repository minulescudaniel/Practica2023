from googleapiclient.discovery import build
import pprint
import requests
from bs4 import BeautifulSoup
import re

my_api_key = "AIzaSyCr6Yvpz6CNLYhZHWn2vrd7QE3GO--ao9o"
my_cse_id = "802c9ced402b44931"
query = input("Introduceți numele: ")


def google_search(search_term, api_key, cse_id, start_index=1, num_results=10, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, start=start_index, num=num_results, **kwargs).execute()
    return res['items']


def get_article_summary(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract the relevant elements from the webpage using BeautifulSoup
        # Customize the code according to the structure of the webpage you are scraping
        possible_summary_names = ["article", "article class article", "div page-title", "product-highlights"]
        for element_name in possible_summary_names:
            summary_element = soup.find(element_name)
            if summary_element:
                return summary_element.get_text().strip()

    return None


def get_price(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Use CSS selectors to target specific HTML elements containing price information
        price_selectors = ["span.price", "div.price", "p.price","div.final-price"]
        for selector in price_selectors:
            price_element = soup.select_one(selector)
            if price_element:
                # Apply regex pattern to extract the price from the element's text
                price_text = price_element.get_text()
                price_pattern = r'\b(\d{1,3}(?:[,.]\d{3})?)\b'
                matches = re.findall(price_pattern, price_text)
                if matches:
                    return matches[0]

    return None

results = google_search(
    f"{query} site:ro", my_api_key, my_cse_id, num_results=10)

for result in results:
    title = result.get('title')
    #price = result.get('pagemap', {}).get('offer', [{}])[0].get('price')
    url = result.get('link')

    #summary = get_article_summary(url)
    summary = ""
    price = get_price(url)

    if title or price or url or summary:
        pprint.pprint(f"Title: {title}")
        pprint.pprint(f"Price: {price}")
        pprint.pprint(f"URL: {url}")
        pprint.pprint(f"Summary: {summary}")
        pprint.pprint("--------------------")
    else:
        pprint.pprint("Incomplete information for this result")

# Retrieve additional results
results = google_search(
    f"{query} site:ro", my_api_key, my_cse_id, start_index=11, num_results=10)

for result in results:
    title = result.get('title')
    #price = result.get('pagemap', {}).get('offer', [{}])[0].get('price')
    url = result.get('link')
    snippet = result.get('snippet')
    summary = " "
    price = get_price(url)

    if title or price or url or summary:
        pprint.pprint(f"Title: {title}")
        pprint.pprint(f"Price: {price}")
        pprint.pprint(f"URL: {url}")
        pprint.pprint(f"Snippet: {snippet}")
        pprint.pprint(f"Summary: {summary}")
        pprint.pprint("===========================================================================")
    else:
        pprint.pprint("Incomplete information for this result")
