import os
import matplotlib.pyplot as plt
import random

print([i for i in range(1,21)])
from grams_extracter_tweet import Text
path = "data/texts_stripped/"
for author in os.listdir(path):
    print(author)
    list = random.sample( os.listdir(path + author), 10)

    for book in list:
        print(book)

        text = Text(open(path + author +  '/' + book, 'r').read())
        text.retrieve_avg_sentence_word()
        print(text.word_len_dis.values())

        plt.plot(  text.word_len_dis.keys(), text.word_len_dis.values(), label= )

    plt.xlabel('input size')
    plt.ylabel('time (s)')
    plt.title( 'meow' )
    plt.grid(True)
    plt.legend()
    plt.show()


    #     #print()
    quit()
