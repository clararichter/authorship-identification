import requests
from bs4 import BeautifulSoup
import csv
import pprint

url ="https://www.gutenberg.org/dirs/GUTINDEX."

def get_books_array():

  books = []

  startYear = 1996
  endYear = 2018
  for year in range(startYear, endYear + 1):
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
              a1 = " ".join(author[:index]).strip()
              a2 = " ".join(author[index +1 :]).strip() #TODO: change for multiple authors
              author = (a1, a2)
          else:
              author = " ".join(author).strip()
          #print(i, " title: ",title, " author: ", author, " no: ", no)
          books.append({"title": title, "author": author, "no": no })
  return books

try:
    filename = 'guttenbooks.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['title', 'author', 'number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        books = get_books_array()
        for book in books:
          writer.writerow({'title': book['title'],'author': book['author'],'number': book['no']})
          #writer.writerow({'author': book['author']})
          #writer.writerow({'number': book['no']})
except csv.Error as e:
    sys.exit('file {}, {}'.format(filename, e))
