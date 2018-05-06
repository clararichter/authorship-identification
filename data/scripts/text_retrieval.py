from urllib.request import urlretrieve
import json
import os

for file in os.listdir("../links"):
    print(file)
    with open('../links/' + file) as f:
        data = json.load(f)
        for book_object in data:
            urlretrieve( book_object['link'], "../texts_raw/{}/{}.txt".format(book_object["author"].split()[1].lower(), book_object["title"].replace(" ", "_").lower()  ) )
