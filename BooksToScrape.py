import requests
from bs4 import BeautifulSoup
import csv

link = "https://books.toscrape.com/catalogue/page-1.html"
session = requests.session()

class Book:
    def __init__(self, t, price, availability):
        self.title = t
        self.price = price
        self.available = availability

    def __str__(self):
        return f"Book: {self.title} for: {self.price}"

    def __repr__(self):
        return f"({self.title}, {self.price})"

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.title, self.price) == (other.title, other.price)
        return False

with open("Results.csv", 'w', newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Titles", "Price", "Availability"])

    while True:
        print(f"Progress: current link -> {link}")
        try:
            page = session.get(link)
            page.encoding = "utf-8"
            soup = BeautifulSoup(page.text, features='lxml')
        except requests.exceptions.HTTPError as e:
            print(f"Error at: {link}. Cannot Continue.")
            print(f"Error: {e}")
            break

        titles = [book.get('title') for book in soup.select("article.product_pod h3 a")]
        prices = [price.text for price in soup.select("div.product_price p.price_color")]
        availables = [available.text.strip() for available in soup.select("p.availability")]

        books = []
        for title, price, available in zip(titles, prices, availables):
            book = Book(title, price, available)
            books.append(book)

        writer.writerows((book.title, book.price, book.available) for book in books)

        next_button = soup.select_one("ul li.next a")
        if next_button:
            link = f"https://books.toscrape.com/catalogue/{next_button.get('href')}"
        else:
            link = None
            print("No new page or button not found")
            break
