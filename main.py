import os
from scraper.scraper_books import BookScraper
from scraper.exporter import export_books_to_csv
from analysis.stats import (
    load_books,
    describe_prices,
    availability_counts,
    summary_by_rating,
    plot_price_histogram,
    plot_price_boxplot,
    price_clustering,
    summary_by_cluster,
    plot_price_clusters,
    plot_cluster_distribution,
    load_custom_products,
    describe_custom_prices,
    price_clustering_custom,
    plot_price_clusters_custom,
    plot_cluster_boxplot_custom,
)

def scraping():
    print("Lancement du scraping des livres...")

    os.makedirs("data", exist_ok=True)

    scraper = BookScraper()
    books = scraper.scrape_all(pages=50)
    print(f"{len(books)} livres récupérés.")

    csv_path = "data/books.csv"
    export_books_to_csv(books, csv_path)
    print(f"Données exportées dans : {csv_path}")

def graphique():
    df = load_books("data/books.csv")

    print("Aperçu du DataFrame :")
    print(df.head())

    describe_prices(df)
    availability_counts(df)
    summary_by_rating(df)

    plot_price_histogram(df)
    plot_price_boxplot(df)

    print("Graphiques enregistrés dans le dossier /data")

    df = price_clustering(df)
    summary_by_cluster(df)
    plot_price_clusters(df)
    plot_cluster_distribution(df)

    print("Graphiques de clustering générés dans le dossier /data")

from scraper.scraper_custom import IkeaSeleniumScraper, export_custom_products

def scrape_ikea_chairs():
    url = "https://www.ikea.com/fr/fr/cat/chaises-700676/"
    scraper = IkeaSeleniumScraper(url)
    products = scraper.scrape()
    print(f"✅ {len(products)} chaises IKEA récupérées.")
    export_custom_products(products, "data/custom_products.csv")

def analyse_custom_products():
    df = load_custom_products("data/custom_products.csv")

    if df.empty:
        print("Fichier custom_products.csv vide ou non trouvé.")
        return

    print(df.head())
    describe_custom_prices(df)

    df = price_clustering_custom(df)
    plot_price_clusters_custom(df)
    plot_cluster_boxplot_custom(df)

    print("Analyse produits personnalisés terminée, fichiers dans /data")

if __name__ == "__main__":
    analyse_custom_products()