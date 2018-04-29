from urllib.request import urlopen, urlretrieve

def spider():
    for i in range(2, 100):
        print("http://www.gutenberg.org/files/{}/{}-h/{}-h.htm".format(i, i, i))
        urlretrieve( "http://www.gutenberg.org/files/{}/{}-h/{}-h.htm".format(i, i, i), "urls/book{}.html".format(i) )


spider()
