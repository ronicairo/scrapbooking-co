import requests
from bs4 import BeautifulSoup
from .book import Book
import time, random
import re

class BookScraper:
    BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
    INDEX_URL = "https://books.toscrape.com/index.html"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    def __init__(self):
        self.books = []

    def scrape_page(self, url):
        try:
            response = requests.get(url, headers=self.HEADERS)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('article.product_pod')
            books_on_page = []

            for article in articles:
                try:
                    title = article.h3.a['title']
                    price_text = article.select_one('.price_color').text.strip()

                    match = re.search(r"\d+\.\d+", price_text)
                    if match:
                        price = float(match.group())
                    else:
                        raise ValueError(f"Format de prix invalide : {price_text}")

                    availability = article.select_one('.availability').text.strip()
                    rating = article.p['class'][1] 

                    book = Book(title, price, availability, rating)
                    books_on_page.append(book)
                except Exception as e:
                    print(f"Livre ignoré à cause d'une erreur : {e}")
                    continue

            return books_on_page

        except Exception as e:
            print(f"Erreur lors du scraping de {url} : {e}")
            return []

    def scrape_all(self, pages=50):
        print("Scraping page d'accueil (index.html)...")
        self.books.extend(self.scrape_page(self.INDEX_URL))

        for page in range(1, pages + 1):
            url = self.BASE_URL.format(page)
            print(f"Scraping {url}...")
            page_books = self.scrape_page(url)
            if not page_books:
                print("Fin du scraping : page vide ou erreur HTTP.")
                break
            self.books.extend(page_books)
            time.sleep(random.uniform(1, 3))

        return self.books
