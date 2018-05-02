import csv
import re

#outfile = open('./gutenberg_books.csv','w')
#writer = csv.DictWriter(outfile, delimiter=' ', quotechar='\t', quoting=csv.QUOTE_MINIMAL)


content = open("head.txt").read()
content = re.sub(' +',' ', content)
content = content.replace(u'\xa0', u' ')

pattern1 = r'\n[A-Za-z0-9 ,.\'()-:]+, by [A-Za-z .-]+ [0-9]+'
pattern2 = r'\n[A-Za-z0-9 ,.\'()-:]+ [0-9]+\n[A-Za-z0-9 ,.\'()-:]+, by [A-Za-z .-]+'

works = re.findall(pattern1, content)
for w in works:
    print(w)
    title = re.search('.+(?=, by)', w)
    author_and_id = re.search('(?<=, by ).+', w)
    author = re.search('.+(?= [0-9]+)', author_and_id[0])
    book_id = re.search('[0-9]+', author_and_id[0])

    print("TITLE: ", title[0])
    print("AUTHOR: ", author[0])
    print("ID: ", book_id[0])
    #writer.writerow( {"title": title[0], "author": author[0], "book_id" : book_id[0]} )

works = re.findall(pattern2, content)
for w in works:
    print(w)
    w = w.replace('\n', ' ')
    author = re.search('(?<=, by ).+', w)

    title_and_id = re.search('.+(?=, by)', w)
    book_id = re.search( r'( (\d+) )', title_and_id[0] )
    #print(title_and_id[0])
    title = re.sub( r'( (\d+) )', 'BLEH', title_and_id[0] )
    print("TITLE: ", title[0])
    print("AUTHOR: ", author[0])
    print("ID: ", book_id[0])
    # #writer.writerow( {"title": title[0], "author": author[0], "book_id" : book_id[0]} )
