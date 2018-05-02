import csv
import re

outfile = open('./gutenberg_books.csv','w')
writer = csv.writer(outfile, delimiter=' ', quotechar='\t', quoting=csv.QUOTE_MINIMAL)


#text = '''\nLucian the dreamer, by J. S. Fletcher                                    55484'''
content = open("catalog.txt").read()
content = re.sub(' +',' ', content)
content = content.replace(u'\xa0', u' ')
#print(content)
pattern = r'\n[A-Za-z0-9 ,.\'()-:]+, by [A-Za-z .-]+ [0-9]+'

works = re.findall(pattern, content)

test = '''
On the Supply of Printed Books from the Library to the Reading 39087
 Room of the British Museum, by Anthony Panizzi
'''

pattern = r'\n[A-Za-z0-9 ,.\'()-:]+ [0-9]+\n[A-Za-z0-9 ,.\'()-:]+, by [A-Za-z .-]+'
works2 = re.findall(pattern, content)

#
# #print(content)
# for w in works:
#     print(w)
print(len(works) + len(works2))
