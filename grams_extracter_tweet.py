import nltk
from nltk.util import ngrams
#from nltk import word_tokenize
from nltk.tokenize import TweetTokenizer, sent_tokenize
import pandas as pd
import numpy as np
class Text():

    def __init__(self, text):
        self.text = text.lower()
        #self.tokens = TweetTokenizer().tokenize(self.text)
        #self.pos_tags = nltk.pos_tag(self.tokens)
        #self.total_number_of_tokens = len(self.tokens)
        self.row = {}
        self.build_row()

        self.sent_len_dis = {}
        self.word_len_dis = {}


    def build_row(self):
        #self.retrieve_gram_data()
        #self.retrieve_pos_data()
        self.retrieve_avg_sentence_word()
        # self.retrieve_word_diversity_data()
        # self.retrieve_word_length_data()
        # self.retrieve_sentence_length_data()


    def retrieve_gram_data(self):
        for n in range(1, 3):
            n_grams = ngrams(self.tokens, n)
            number_of_n_grams = self.total_number_of_tokens - n + 1
            self.row.update( { " ".join(n_gram) : (lambda count: count / number_of_n_grams)(count) for ( n_gram, count ) in self.count_map(n_grams).items() } )

    def count_map(self, items):
        count_map = {}
        for item in items:
            if item in count_map:
                count_map[item] += 1
            else:
                count_map[item] = 1
        return count_map


    def retrieve_pos_data(self):
        for n in range(1, 3):
            pos_n_grams = []
            for i in range(0, len(self.pos_tags)+1-n):
                pos_n_grams.append( tuple([ tag for (word, tag) in  self.pos_tags[i:i+n]]) )
            self.row.update( {  " ".join(pos_n_gram) : (lambda count: count / len(pos_n_grams))(count) for ( pos_n_gram, count ) in self.count_map(pos_n_grams).items() } )


    def retrieve_avg_sentence_word(self):
        sent_tokenize_list = sent_tokenize(self.text)
        #length count map
        sent_length = []
        word_length = []
        for sent in sent_tokenize_list:
            count = 0
            for word in TweetTokenizer().tokenize(sent):
                punt = [".", ",", "?", "!", "\"","\'",";",":"]
                if word not in punt:
                    count += 1
                    word_length.append(len(word))
            sent_length.append(count)
        self.sent_len_dis = self.count_map(sorted(sent_length))
        self.word_len_dis = self.count_map(sorted(word_length))

        avg_sent_length = np.mean(sent_length)
        avg_word_length = np.mean(word_length)
        # return (avg_sent_length, avg_word_length)
        self.row.update({ "avg_sent_length": avg_sent_length, "avg_word_length": avg_word_length})
        print (float("%.2f" % avg_sent_length), float("%.2f" % avg_word_length))






def main():
    matrix = pd.DataFrame()

    para1 = """
        Marley was dead, to begin with. There is no doubt whatever about that.
        The register of his burial was signed by the clergyman, the clerk, the
        undertaker, and the chief mourner. Scrooge signed it. And Scrooge's name
        was good upon 'Change for anything he chose to put his hand to. Old
        Marley was as dead as a door-nail.
    """
    para2 = """
        Scrooge knew he was dead? Of course he did. How could it be otherwise?
        Scrooge and he were partners for I don't know how many years. Scrooge
        was his sole executor, his sole administrator, his sole assign, his sole
        residuary legatee, his sole friend, and sole mourner. And even Scrooge
        was not so dreadfully cut up by the sad event but that he was an
        excellent man of business on the very day of the funeral, and solemnised
        it with an undoubted bargain.
    """
    books_df = pd.DataFrame()
    paras = [para1, para2]
    for i in range(0, len(paras)):
        print(i)
        text = Text(paras[i])
        index = "para"+ str(i)
        book_df = pd.DataFrame(text.row,index =[index])
        books_df = books_df.append(book_df)
    with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
        print(books_df)

    # books = ["a_bullet_for_cinderella_49931", "a_child's_dream_of_a_star_42232"]
    # #books = ["a_bullet_for_cinderella_49931"]
    #
    # base = "ice_box/publish_date_books/books/"
    # file_type = ".txt"
    # for book in books:
    #     dic = base + book + file_type
    #     file = open(dic,'r')
    #     text = Text(file.read())
    #     #text = Text(" the beautiful cat sits. the beautiful cat sits ")
    #     text.build_row()
    #     book_df = pd.DataFrame(text.row,index =[book])
    #     matrix = matrix.append(book_df)
    # #with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    #     #print(matrix)


if __name__ == '__main__':
    main()
