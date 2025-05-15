import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

def load_books(filepath):
    try:
        df = pd.read_csv(filepath)

        # Nettoyage : suppression du symbole £ si jamais il est resté
        df['price'] = df['price'].astype(str).str.replace('£', '', regex=False)

        # Conversion en float
        df['price'] = df['price'].astype(float)

        return df
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return pd.DataFrame()

def describe_prices(df):
    print("Statistiques descriptives sur les prix :")
    print(df['price'].describe())

def availability_counts(df):
    print("\Disponibilité des livres :")
    print(df['availability'].value_counts())

    print("\n⭐ Répartition par rating :")
    print(df['rating'].value_counts())

def summary_by_rating(df):
    print("Prix moyen par niveau de rating :")
    print(df.groupby('rating')['price'].mean())

import matplotlib.pyplot as plt
import os

def plot_price_histogram(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
    plt.title("Histogramme des prix des livres")
    plt.xlabel("Prix (£)")
    plt.ylabel("Nombre de livres")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/histogram_price.png")
    plt.close()

def plot_price_boxplot(df):
    plt.figure(figsize=(6, 4))
    plt.boxplot(df['price'])
    plt.title("Boxplot des prix")
    plt.ylabel("Prix (£)")
    plt.tight_layout()
    plt.savefig("data/boxplot_price.png")
    plt.close()

def price_clustering(df, n_clusters=3):
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    df['price_cluster'] = model.fit_predict(df[['price']])
    return df

def summary_by_cluster(df):
    print("Statistiques par cluster de prix :")
    print(df.groupby('price_cluster')['price'].describe())

def plot_price_clusters(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df.index, df['price'], c=df['price_cluster'], cmap='viridis')
    plt.title("Clustering des prix (KMeans)")
    plt.xlabel("Index")
    plt.ylabel("Prix (£)")
    plt.tight_layout()
    plt.savefig("data/clustering_price.png")
    plt.close()

def plot_cluster_distribution(df):
    plt.figure(figsize=(7, 5))
    df.boxplot(column='price', by='price_cluster')
    plt.title("Boxplot des prix par cluster")
    plt.suptitle("")
    plt.xlabel("Cluster")
    plt.ylabel("Prix (£)")
    plt.tight_layout()
    plt.savefig("data/cluster_boxplot.png")
    plt.close()

def load_custom_products(filepath):
    try:
        df = pd.read_csv(filepath)
        df['price'] = df['price'].astype(str).str.replace(',', '.').astype(float)
        return df
    except Exception as e:
        print(f"Erreur chargement custom products : {e}")
        return pd.DataFrame()

def describe_custom_prices(df):
    print("Statistiques descriptives des prix produits personnalisés :")
    print(df['price'].describe())

def price_clustering_custom(df, n_clusters=3):
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    df['price_cluster'] = model.fit_predict(df[['price']])
    return df

def plot_price_clusters_custom(df):
    plt.figure(figsize=(8,5))
    plt.scatter(df.index, df['price'], c=df['price_cluster'], cmap='plasma')
    plt.title("Clustering des prix produits personnalisés")
    plt.xlabel("Index")
    plt.ylabel("Prix (€)")
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/clustering_custom_products.png")
    plt.close()

def plot_cluster_boxplot_custom(df):
    plt.figure(figsize=(7,5))
    df.boxplot(column='price', by='price_cluster')
    plt.title("Boxplot des prix par cluster - produits personnalisés")
    plt.suptitle("")
    plt.xlabel("Cluster")
    plt.ylabel("Prix (€)")
    plt.savefig("data/boxplot_cluster_custom_products.png")
    plt.close()