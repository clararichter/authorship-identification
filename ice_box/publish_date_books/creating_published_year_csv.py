import get_published_date
import csv
import sys


def list_books():
  filename = 'guttenbooks.csv'
  try:
    with open(filename, 'r') as f:
      reader = csv.reader(f)
      next(reader, None)
      book_info = []
      for row in reader:
        book_info.append([row[0], row[1], row[2]])
      # book_info = [[row[0], row[1], row[2]] for row in reader]
      return book_info
  except csv.Error as e:
    sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))


books_array = list_books()
count = 0
for book in books_array:
  count += 1
  if count % 100 == 0:
    sys.stdout.write('.')
  print("pre_google_call_book", book[0], book[1])
  pub_date = get_published_date.find_book(title = str(book[0]), author = str(book[1]))
  print("post_google_call_book", book[0], book[1], pub_date)  
  book.append(pub_date)

try:
    with open('guttenbookspub.csv', 'w', newline='') as csvfile:
      fieldnames = ['title', 'author', 'number', 'pubyear']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for book in books_array:
        writer.writerow({'title': book[0],'author': book[1], 'no': book[2], 'pubyear': book[3]})
except csv.Error as e:
    sys.exit('file {}, {}'.format(filename, e))
