import csv
import re
import requests


# from urllib.request import urlretrieve
# urlretrieve( "http://www.gutenberg.org/dirs/GUTINDEX.ALL", "gutenberg_catalog_ALL.txt" )
def get_link(book_id):
    link = "http://www.gutenberg.org/files/{}/{}.txt".format(book_id, book_id)
    if requests.get(link).status_code == 200:
        return link
    link = "http://www.gutenberg.org/files/{}/{}-0.txt".format(book_id, book_id)
    if requests.get(link).status_code == 200:
        return link
    link = "http://www.gutenberg.org/cache/epub/{}/pg{}.txt".format(book_id, book_id)
    if requests.get(link).status_code == 200:
        return link

    return "LINK NOT FOUND"


outfile = open('../books.csv', 'w')
writer = csv.DictWriter(outfile, fieldnames=['title', 'author', 'book_id', 'link'])

books = []
file = open("../authors.txt", 'r')
authors = file.read().split('\n')

content = open("../gutenberg_catalog_ALL.txt").read()
content = re.sub(' +', ' ', content)
content = content.replace(u'\xa0', u' ')
content = re.sub(r'\[#[0-9]+\]*\[.*\]', '', content)
content = re.sub(r'Audio.*\n', '', content)

p1 = r'\n.*[\n ]+\[Language: .*\n'
p2 = r'.*\n \[.*\][\n ]+\[Language: .*'
p3 = r'.*\n \[.*\][\n ]+\[.*\][\n ]+\[Language: .*'
p4 = r'.*\n \[Language .*'
p5 = r'.*\n \[.*\][\n ]+\[Language .*'
p6 = r'.*\n \[.*\][\n ]+\[.*\][\n ]+\[Language .*'

content = re.sub(p1, '', content)
content = re.sub(p2, '', content)
content = re.sub(p3, '', content)
content = re.sub(p4, '', content)
content = re.sub(p5, '', content)
content = re.sub(p6, '', content)

pattern1 = r'\n[A-Za-z0-9 ,.\'\"()-:?&$]+, by [A-Za-zë .,]+ [0-9]+'
pattern2 = r'\n[A-Za-z0-9 ,.\'\"()-:?&$]+ [0-9]+\n[A-Za-z0-9 ,.\'\"()-:&$]+, by [A-Za-zë .,]+'

works = re.findall(pattern1, content)

for w in works:
    title = re.search('.+(?=, by)', w)
    author_and_book_id = re.search('(?<=, by ).+', w)
    author = re.search('.+(?= [0-9]+)', author_and_book_id[0])
    book_id = re.search('[0-9]+', author_and_book_id[0])

    if author[0] in authors:
        print("TITLE: ", title[0])
        print("AUTHOR: ", author[0])
        print("book_id: ", book_id[0])
        link = get_link(book_id[0])

        print("LINK: ", link)
        print()
        writer.writerow({'author': author[0], 'title': title[0], 'book_id': book_id[0], 'link': link})

content = re.sub(pattern1, '', content)

works = re.findall(pattern2, content)
for w in works:
    book_id = re.search(r'[0-9]+(?=\n)', w)
    w = w.replace('\n', ' ')
    author = re.search('(?<=, by )[A-Za-z .-]+', w)
    title = re.search('.+(?=, by)', w)
    title = re.sub(r' (\d+) ', '', title[0])

    if author[0] in authors:
        print("TITLE: ", title)
        print("AUTHOR: ", author[0])
        print("book_id: ", book_id[0])
        link = get_link(book_id[0])

        print("LINK: ", link)
        print()
        writer.writerow({'author': author[0], 'title': title, 'book_id': book_id[0], 'link': link})

content = re.sub(pattern2, '', content)
