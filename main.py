import requests
from bs4 import BeautifulSoup
import csv
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import threading
import schedule
import time
from tkinter import scrolledtext


def send_email(subject, body):
    sender_email = "danielpractica24@gmail.com"
    sender_password = "frotqrynsgabiznx"
    receiver_email = "minulescudaniel@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)


def search(page_number=0):
    global status_label
    global grouped_products

    query = entry.get()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
    url = f"https://www.google.com/search?q={query}&tbm=shop&start={page_number * 10}"
    r = requests.get(url, headers=headers, cookies=cookies)

    print("Executing program with query: " + query + ", page: " + str(page_number))

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
                previous_prices[product_key].append(re.sub(r"\D", "", row["Pret"]))  # Remove non-digit characters
    except FileNotFoundError:
        previous_prices = {}

    with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(csv_header)

        best_deal = None

        grouped_products = {}

        # Extract product information from each container
        for container in product_containers:
            title_element = container.find("div", class_="EI11Pd")
            title = title_element.text.strip() if title_element else ""

            price_element = container.find("span", class_="a8Pemb OFFNJ")
            price = price_element.text.strip() if price_element else ""

            second_hand_element = container.find("span", class_="tD1ls")
            second_hand = second_hand_element.text.strip() if second_hand_element else "Nou"

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
                    price_history.append(re.sub(r"\D", "", price))  # Remove non-digit characters

                    # Check if it's the best deal
                    if best_deal is None or price < best_deal["price"]:
                        best_deal = {
                            "title": title,
                            "price": price,
                            "second_hand": second_hand,
                            "store": store,
                            "url": url,
                            "timestamp": timestamp
                        }

            else:
                previous_prices[product_key] = [re.sub(r"\D", "", price)]  # Remove non-digit characters

            if title in grouped_products:
                grouped_products[title].append({
                    "Price": price,
                    "Condition": second_hand,
                    "Store": store,
                    "URL": url,
                    "Timestamp": timestamp
                })
            else:
                grouped_products[title] = [{
                    "Price": price,
                    "Condition": second_hand,
                    "Store": store,
                    "URL": url,
                    "Timestamp": timestamp
                }]

            row = [title, price, second_hand, store, url, timestamp]
            writer.writerow(row)

    if best_deal:
        price_formatted = f"{best_deal['price']}"
        subject = "Oferta: " + best_deal["title"]
        body = f"Nume: {best_deal['title']}\n" \
               f"Pret: {price_formatted}\n" \
               f"Conditie: {best_deal['second_hand']}\n" \
               f"Magazin: {best_deal['store']}\n" \
               f"URL: {best_deal['url']}\n" \
               f"Data: {best_deal['timestamp']}"
        send_email(subject, body)

    status_label.configure(text="Datele s-au salvat in " + csv_filename)

    display_grouped_products(grouped_products)


def display_grouped_products(grouped_products):
    global result_frame
    global tree
    global scroll_text

    if result_frame:
        result_frame.destroy()

    result_frame = ttk.Frame(window)
    result_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree = ttk.Treeview(result_frame, columns=("Product Name",))
    tree.heading("#0", text="")
    tree.heading("Product Name", text="Product Name")
    tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
    tree.column("Product Name", stretch=tk.YES, width=500)

    for index, product_name in enumerate(grouped_products):
        tree.insert(parent="", index=index, iid=index, text="", values=(product_name,))

    tree.bind("<<TreeviewSelect>>", on_treeview_select)
    tree.pack(fill="both", expand=True)

    scroll_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=10)
    scroll_text.pack(fill="both", expand=True, pady=10)
    scroll_text.configure(state="disabled")


def on_treeview_select(event):
    selected_item = event.widget.selection()[0]
    product_name = event.widget.item(selected_item, "values")[0]

    products = grouped_products[product_name]

    scroll_text.configure(state="normal")
    scroll_text.delete(1.0, tk.END)

    for product in products:
        price_formatted = f"{product['Price']}"
        scroll_text.insert(tk.END, f"Nume: {product_name}\n"
                                   f"Pret: {price_formatted}\n"
                                   f"Conditie: {product['Condition']}\n"
                                   f"Magazin: {product['Store']}\n"
                                   f"URL: {product['URL']}\n"
                                   f"Data: {product['Timestamp']}\n\n")

    scroll_text.configure(state="disabled")


def start_search():
    global status_label
    status_label.configure(text="Cautare in desfasurare...")
    threading.Thread(target=search).start()


def schedule_search():
    schedule.every(1).hours.do(start_search)

    while True:
        schedule.run_pending()
        time.sleep(1)


window = ThemedTk(theme="arc")
window.geometry("1300x600")
window.title("Web Scraper")

query_frame = ttk.Frame(window)
query_frame.pack(pady=20)

label = ttk.Label(query_frame, text="Introduceti un produs:")
label.pack(side="left")

entry = ttk.Entry(query_frame)
entry.pack(side="left")

search_button = ttk.Button(query_frame, text="Cauta", command=start_search)
search_button.pack(side="left", padx=10)

status_label = ttk.Label(window, text="")
status_label.pack(pady=10)

result_frame = None
tree = None
scroll_text = None

next_page_button = ttk.Button(window, text="Pagina urmatoare", command=lambda: threading.Thread(target=search, args=(1,)).start())
next_page_button.pack(pady=10)

threading.Thread(target=schedule_search).start()

window.mainloop()
