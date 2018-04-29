from urllib.request import urlopen, urlretrieve

def spider():
    for i in range(2, 100):
        print("http://www.gutenberg.org/files/{}/{}-h/{}-h.htm".format(i, i, i))
        urlretrieve( "http://www.gutenberg.org/files/{}/{}.txt".format(i, i), "urls/book{}.txt".format(i) )


        #"http://www.gutenberg.org/files/{}/{}-h/{}-h.htm".format(i, i, i)
spider()
