from urllib.request import urlretrieve
import csv
import os

with open('books.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for book in reader:

        if book[3] != "LINK NOT FOUND":
            print(book[3], "--->\n",
                  "../texts_raw/{}/{}.txt".format(book[1].lower().replace(" ", '_'), book[0].replace(" ", "_").lower()))
            directory = "../texts_raw/{}".format(book[1].lower().replace(" ", "_"))
            if not os.path.exists(directory):
                os.makedirs(directory)

            urlretrieve(book[3], "../texts_raw/{}/{}.txt".format(book[1].lower().replace(" ", '_'),
                                                                 book[0].replace(" ", "_").lower()))
