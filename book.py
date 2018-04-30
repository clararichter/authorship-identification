import requests
from bs4 import BeautifulSoup
import csv
import pprint

url ="https://www.gutenberg.org/dirs/GUTINDEX."

books = dict()

startYear = 1996
endYearPlus1 = 1997
for year in range(startYear, endYearPlus1):
    print(year)
    page = requests.get(url + str(year))
    soup = BeautifulSoup(page.content, 'html.parser')

    w = []
    for string in soup.strings:
        w.append(repr(string))
    rows = w[0].split("NO.")[1].split("\\r\\n\\r\\n")

    for i in range(1,len(rows)):

        comma = True
        row = rows[i].split("by") #TODO: mutiple "by"'s cause incorrect split
        if len(row) == 1:
            row = rows[i].split(",")
            comma = False

        title = row[0].strip()

        if comma:
            title = title[:-1]

        if len(row) == 1:
            continue #no author

        subtitle = row[1].split("\\r\\n")
        info = subtitle[0].split()

        if len(info) == 0: #empty, I don't know why this can happen
            continue

        #print(info)
        no = info[len(info)-1]
        try:
            int(no) #check if there is no.
            author = info[:len(info)-1]
            #TODO: if title is too long, no. is in between of title and author
        except ValueError:
            author = info
            no = "NaN"

        if "and" in author:
            index = author.index("and")
            a1 = " ".join(author[:index])
            a2 = " ".join(author[index +1 :]) #TODO: change for multiple authors
            author = (a1, a2)
        else:
            author = " ".join(author)
        #print(i, " title: ",title, " author: ", author, " no: ", no)
        books[title] = {"author": author, "no": no }

#pprint.pprint(books)
print(len(books))
