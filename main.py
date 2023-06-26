import requests
from bs4 import BeautifulSoup
import csv
import datetime
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import threading
import schedule
import time


def search():
    global status_label

    query = entry.get()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
    r = requests.get(f"https://www.google.com/search?q={query}&tbm=shop", headers=headers, cookies=cookies)

    url = f"https://www.google.com/search?q={query}&tbm=shop"

    print("Se executa programul cu query-ul: " + query)

    soup = BeautifulSoup(r.content, "html.parser")

    product_containers = soup.find_all("div", class_="sh-dgr__content")

    csv_filename = "price_history.csv"
    csv_header = ["Nume", "Pret", "Stare", "Magazin", "URL", "Timestamp"]

    previous_prices = {}

    try:
        with open(csv_filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_key = (row["Nume"], row["Magazin"])
                if product_key not in previous_prices:
                    previous_prices[product_key] = []
                previous_prices[product_key].append(row["Pret"])
    except FileNotFoundError:
        previous_prices = {}

    with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(csv_header)

        # Extract product information from each container
        for container in product_containers:
            title_element = container.find("div", class_="EI11Pd")
            title = title_element.text.strip() if title_element else ""

            price_element = container.find("span", class_="a8Pemb OFFNJ")
            price = price_element.text.strip() if price_element else ""

            second_hand_element = container.find("span", class_="tD1ls")
            second_hand = second_hand_element.text.strip() if second_hand_element else ""

            store_element = container.find("div", class_="aULzUe IuHnof")
            store = store_element.text.strip() if store_element else ""

            url_element = container.find("a", class_="xCpuod")
            url = url_element["href"] if url_element else ""
            url = "https://www.google.com" + url

            timestamp = datetime.datetime.now()

            product_key = (title, store)
            if product_key in previous_prices:
                price_history = previous_prices[product_key]
                if price not in price_history:
                    price_history.append(price)

            else:
                previous_prices[product_key] = [price]

            row = [title, price, second_hand, store, url, timestamp]
            writer.writerow(row)

    status_label.configure(text="Data has been saved to the file " + csv_filename)


window = ThemedTk(theme="radiance")
window.title("Price Tracker")
window.geometry("400x200")


search_frame = ttk.Frame(window, padding="20")
search_frame.pack()


search_label = ttk.Label(search_frame, text="Search:")
search_label.pack(side="left")


entry = ttk.Entry(search_frame, width=30)
entry.pack(side="left")


button = ttk.Button(search_frame, text="Search", command=search)
button.pack(side="left", padx=10)

status_label = ttk.Label(window, text="")
status_label.pack(pady=10)


def search_job():
    search()


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every(60).minutes.do(search_job)  # Run search_job() every 60 minutes

thread = threading.Thread(target=run_schedule)
thread.daemon = True  # Se seteaza thread-ul ca daemon pentru a opri procesele cand se termina programul principal
thread.start()

window.mainloop()
