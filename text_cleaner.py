import nltk
from urllib.request import urlopen, urlretrieve
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt
#from nltk.tokenize import RegexpTokenizer
#from nltk.tokenize import regexp_tokenize, wordpunct_tokenize, blankline_tokenize
import re
import pandas as pd

def plot_hist(df, columns):
    df[columns].hist(color='r', alpha=0.1, normed=False)


def main():
    file=open("test_book.txt",'r')
    print(type(file))
    s = ""
    for c in file:
        s+=c
    tknzr = TweetTokenizer()

    tokens = tknzr.tokenize(s)
    fdist = nltk.FreqDist(tokens)
    print(dict(fdist).values())
    d = {'word': list(dict(fdist).keys()), 'frequency':list(dict(fdist).values())}

    df = pd.DataFrame(d, columns=['word', 'frequency'])
    df = df.sort_values(by='frequency')
    #print(df)
    print(len(df))
    f = df.tail(50)

    plot_hist()
    # print(f)
    #
    # probs = []
    #
    # for i in range(50):
    #     print(f.iloc[i].frequency)
    #     probs.append(f.iloc[i].frequency)
    #
    # plt.plot( [i for i in range(50)], probs)
    #
    # plt.xlabel('word', fontsize=14)
    # plt.ylabel('Probability that developer is of job level X', fontsize=14)
    # plt.grid(True)
    # plt.show()


    urlretrieve( "http://www.gutenberg.org/files/1342/1342-0.txt", "book.txt" )





#    print(tokens)

if __name__ == '__main__':
    main()
