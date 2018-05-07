from urllib.request import urlretrieve
import csv

with open('books.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for book in reader:
        print(book['author'])

#
# for file in os.listdir("../links"):
#     print(file)
#     with open('../links/' + file) as f:
#         data = json.load(f)
#         for book_object in data:
#             urlretrieve( book_object['link'], "../texts_raw/{}/{}.txt".format(book_object["author"].split()[1].lower(), book_object["title"].replace(" ", "_").lower()  ) )
