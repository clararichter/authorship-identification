import ast
import csv

file = open('books_publicationdate_dictionaries.txt')



#print(books_array)

outfile = open('./goodreads_catalog.csv','w')
fieldnames = ['title', 'author', 'pub_year']
writer = csv.DictWriter(outfile, fieldnames=fieldnames)



#books_array = []
for line in file:
  d = (ast.literal_eval(line))
  writer.writerow({'title':d['title'], 'author':d['author'][0], 'pub_year':d['date']})
  # books_array.append(dict(line))
