import csv

def export_books_to_csv(books, filepath):
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'price', 'availability', 'rating']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for book in books:
                writer.writerow(book.to_dict())

        print(f"Exportation réussie vers {filepath}")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
