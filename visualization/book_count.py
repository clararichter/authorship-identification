import os

def get_book_count_data():
    book_counts = []
    path = "../data/texts_stripped/"
    for author_folder in os.listdir(path):
        book_counts.append(len(os.listdir(path + author_folder)))
    return ( os.listdir(path), book_counts )
