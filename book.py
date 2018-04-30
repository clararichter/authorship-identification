import requests
from bs4 import BeautifulSoup
import csv
import pprint

url ="https://www.gutenberg.org/dirs/GUTINDEX."

books = dict()

for year in range(1996, 2019):
    print(year)
    page = requests.get(url + str(year))
    soup = BeautifulSoup(page.content, 'html.parser')



    w = []
    for string in soup.strings:
        w.append(repr(string))
    rows = w[0].split("NO.")[1].split("\\r\\n\\r\\n")

    for i in range(1,len(rows)):

        comma = True
        row = rows[i].split("by")
        if len(row) == 1:
            row = rows[i].split(",")
            comma = False
        title = row[0].strip()
        if comma:
            title = title[:-1]
        #print(i, " ",row)

        if len(row) == 1:
            continue#no author
        subtitle = row[1].split("\\r\\n")
        #author = " ".join(subtitle[0].split())
        info = subtitle[0].split()
        if len(info) == 0:
            continue #empty
        #print(info)
        no = info[len(info)-1]
        try:
            int(no)
            author = info[:len(info)-1]
        except ValueError:
            author = info
            no = "NaN"

        if "and" in author:
            index = author.index("and")
            a1 = " ".join(author[:index])
            a2 = " ".join(author[index +1 :])
            author = (a1, a2)
        else:
            author = " ".join(author)
        #print(i, " title: ",title, " author: ", author, " no: ", no)
        books[title] = {"author": author, "no": no }

#pprint.pprint(books)
print(len(books))
