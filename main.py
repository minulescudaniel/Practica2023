import requests
from bs4 import BeautifulSoup
import csv
import datetime

# Define the search query
query = input("Search: ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
r = requests.get(
    f"https://www.google.com/search?q={query}&tbm=shop", headers=headers, cookies=cookies
)

# Send a GET request to Google Shopping search results page
url = f"https://www.google.com/search?q={query}&tbm=shop"

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(r.content, "html.parser")

# Find the product containers on the page
product_containers = soup.find_all("div", class_="sh-dgr__content")

# Prepare the CSV file for writing
csv_filename = "price_history.csv"
csv_header = ["Nume", "Pret", "Stare", "Magazin", "URL", "Timestamp"]

# Create a dictionary to store the previously recorded prices
previous_prices = {}

try:
    # Read the previously recorded prices from the CSV file
    with open(csv_filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            previous_prices[row["Nume"]] = row["Pret"]
except FileNotFoundError:
    # If the CSV file is not found, initialize an empty dictionary
    previous_prices = {}

# Prepare the CSV file for writing
with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    if csvfile.tell() == 0:
        writer.writerow(csv_header)

    # Extract product information from each container
    for container in product_containers:
        # Extract the title
        title_element = container.find("div", class_="EI11Pd")
        title = title_element.text.strip() if title_element else ""

        # Extract the price
        price_element = container.find("span", class_="a8Pemb OFFNJ")
        price = price_element.text.strip() if price_element else ""

        second_hand_element = container.find("span", class_="tD1ls")
        second_hand = second_hand_element.text.strip() if second_hand_element else ""

        # Extract the store
        store_element = container.find("div", class_="aULzUe IuHnof")
        store = store_element.text.strip() if store_element else ""

        url_element = container.find("a", class_="xCpuod")
        url = url_element["href"] if url_element else ""
        url = "https://www.google.com" + url

        # Get the current timestamp
        timestamp = datetime.datetime.now()

        # Print or process the product information as desired
        print("Nume:", title)
        print("Pret:", price)
        if second_hand == "":
            second_hand = "Nou"
        print("Stare:", second_hand)
        print("Magazin:", store)
        print("URL:", url)
        print("---------------------")

        # Check if the price has changed for the current product
        if title in previous_prices:
            previous_price = previous_prices[title]
            if previous_price != price:
                if float(previous_price.replace(",", "")) > float(price.replace(",", "")):
                    print("Price has changed for", title)
                    print("Previous price:", previous_price)
                    print("Current price:", price)
                    print("---------------------")

        # Write the product information to the CSV file
        row = [title, price, second_hand, store, url, timestamp]
        writer.writerow(row)

print("Datele s-au salvat in fisierul csv", csv_filename)



