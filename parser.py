import csv
import re

url ="https://www.gutenberg.org/dirs/GUTINDEX."

outfile = open('./gutenberg_catalog.csv','w')
writer = csv.writer(outfile, delimiter=' ', quotechar='\t', quoting=csv.QUOTE_MINIMAL)

for year in range(1996, 2019):
    content = repr(open("catalogs/year{}.txt".format(year)).read())
    works = content.split('\\n\\n')


    for i in range(0,len(works)):
        original = works[i]
        book_id = re.findall(r' [0-9]+', works[i])
        if book_id:
            book_id = book_id[0].rstrip('  ')

            works[i] = re.sub(r'  [0-9]+C?', "", works[i])
            works[i] = re.sub(r'(  )+(.)*', "", works[i])
            works[i] = re.sub(r'\\xa0', "", works[i])
            works[i] = re.sub(r'\'\\ufeff', "", works[i])
            works[i] = re.sub(r'\\', "", works[i])

            tokens = re.split(r', by', works[i])
            for i in range(len(tokens)):
                tokens[i] = tokens[i].strip()

            # if len(tokens) > 1:
            #     tokens.append(book_id)
            # else:
            #     tokens.append("UNKNOWN")
            #     tokens.append(book_id)
            # print(type(tokens[2]))
            writer.writerow([tokens[0].strip(), book_id.strip()])
