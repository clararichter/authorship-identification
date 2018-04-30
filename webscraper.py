import csv, sys, nltk, requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
import pprint

#TODO: README file -> python3 -m nltk.downloader all (try to see if we need this)
#NLTK comes with many corpora, toy grammars, trained models, etc.

class Webscraper():

    def __init__(self, url):
        self.contractions = self.list_contractions()
        self.words = self.scraper(url)
        self.word_freq = self.freq_dist(self.words)

    def scraper(self, url):
        page = requests.get(url)

        if page.status_code == requests.codes.ok:

            soup = BeautifulSoup(page.content, 'html.parser')

            limit = 50
            p_tags = soup.find_all('p', limit = limit)
            words = []
            start = int(len(p_tags)/2)

            words_needed = 500
            for num in range(start, limit):
                paragraph = p_tags[num].get_text()
                words += self.words_processing(paragraph.split(" "))
                if len(words) >= words_needed:
                    return words

            return False #TODO: raise error for no enough words

        #TODO: raise error for base status code


    def freq_dist(self, words):
        return nltk.FreqDist(words)

    def words_processing(self, words):
        allow_words = []

        for w in words:
            if w in self.contractions:
                allow_words.append(w)
            else:
                allow_words += [word for word in word_tokenize(w) if word.isalpha()]

        #allow_words = [word.lower() for word in allow_words]
        return allow_words


    def list_contractions(self):
        filename = 'contractions.csv'
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
                contractions = [row[0] for row in reader]
            return contractions
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

x = Webscraper("http://www.gutenberg.org/files/40362/40362-h/40362-h.htm")
#pprint.pprint(x.words)

#f = x.word_freq
#print(f.most_common(2))
#print(f.keys)
#sorted(f) give list of sorted keys
# for k,v in f.items():
#     print (k,v)

#con = x.contractions
#print(con)



#testing contractions

# mytext = "Hello Mr. Adam, how are you? hasn't [2]."
# tokens = word_tokenize(mytext)
# print(tokens)
# words = [word for word in tokens if word.isalpha()]
# print(words)
#
#
# tokens = mytext.split(" ")
# print(tokens)
# good_words = []
# for x in tokens:
#     if x in con:
#         good_words.append(x)
#     else:
#         good_words += [word for word in word_tokenize(x) if word.isalpha()]
# print(good_words)
