from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import os

class IkeaSeleniumScraper:
    def __init__(self, url, max_scroll=5):
        self.url = url
        self.max_scroll = max_scroll
        self.products = []

    def scrape(self):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        # Scroll pour charger tous les produits
        for _ in range(self.max_scroll):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        product_divs = driver.find_elements(By.CSS_SELECTOR, "div.plp-mastercard")

        for div in product_divs:
            try:
                title = div.find_element(By.CSS_SELECTOR, "span.plp-price-module__product-name").text.strip()
                desc = div.find_element(By.CSS_SELECTOR, "span.plp-price-module__description").text.strip()
                price_int = div.find_element(By.CSS_SELECTOR, "span.plp-price__integer").text.strip()
                price_dec = div.find_element(By.CSS_SELECTOR, "span.plp-price__decimal").text.strip()
                price_str = price_int + "." + price_dec.replace(",", "")  # Ex: "89" + "99" -> "89.99"
                price = float(price_str)

                try:
                    availability = div.find_element(By.CSS_SELECTOR, "span.plp-status__label").text.strip()
                except:
                    availability = "Indisponible"

                product = {
                    "title": title,
                    "description": desc,
                    "price": price,
                    "availability": availability
                }
                self.products.append(product)
            except Exception as e:
                print(f"Produit ignoré à cause de l’erreur : {e}")

        driver.quit()
        return self.products

def export_custom_products(products, filepath):
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["title", "description", "price", "availability"]
        import csv
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for prod in products:
            writer.writerow(prod)

