from nltk.util import ngrams
from nltk.tokenize import TweetTokenizer, sent_tokenize
import pandas as pd
import numpy as np

class Text():

    def __init__(self, text):
        self.text = text.lower()
        self.tokens = TweetTokenizer().tokenize(self.text)
        self.sentences = sent_tokenize(self.text)
        self.total_number_of_tokens = len(self.tokens)
        self.row = {}
        #self.build_row()

    def build_row(self):
        self.word_richness()
        self.word_length_data()
        self.sentence_length_data()
        self.num_sentences()
        self.gram_data()
        self.pos_data()

    def count_map(self, items):
        count_map = {}
        for item in items:
            if item in count_map:
                count_map[item] += 1
            else:
                count_map[item] = 1
        return count_map

    def percentage_map(self, count_map, total):
        return( { key : (lambda count: count / total)(count) for ( key, count ) in count_map.items() } )

    def gram_data(self):
        n = 3
        for n in range(1, n):
            n_grams = ngrams(self.tokens, n)
            number_of_n_grams = self.total_number_of_tokens - n + 1
            self.row.update( { " ".join(n_gram) : (lambda count: count / number_of_n_grams)(count) for ( n_gram, count ) in self.count_map(n_grams).items() } )

    def pos_data(self):
        n = 3
        pos_tags = nltk.pos_tag(self.tokens)
        for n in range(1, n):
            pos_n_grams = []
            for i in range(0, len(pos_tags)+1-n):
                pos_n_grams.append( tuple([ tag for (word, tag) in  pos_tags[i:i+n]]) )
            self.row.update( {  " ".join(pos_n_gram) : (lambda count: count / len(pos_n_grams))(count) for ( pos_n_gram, count ) in self.count_map(pos_n_grams).items() } )

    def word_lengths(self):
        word_lengths = []
        forbidden = [".", ",", "?", "!", "\"","\'",";",":"]
        for word in self.tokens:
            if word not in forbidden:
                word_lengths.append(len(word))
        return sorted(word_lengths)

    def sentence_lengths(self):
        sentence_lengths = []
        for sentence in self.sentences:
            sentence_lengths.append(len(sentence.split(" ")))
        return sorted(sentence_lengths)

    def word_length_distr(self):
        word_lengths = self.word_lengths()
        return self.percentage_map( self.count_map(word_lengths), len(word_lengths) )

    def sentence_lengths_distr(self):
        sentence_lengths = self.sentence_lengths()
        return self.percentage_map( count_map(sentence_lengths), len(sentence_lengths) )

    def word_length_data(self):
        word_lengths = self.word_lengths()
        self.row.update( {'word_length_avg': np.mean(word_lengths),'word_length_std_dev': np.std(word_lengths)} )

    def sentence_length_data(self):
        sentence_lengths = self.sentence_lengths()
        self.row.update( {'sentence_length_avg': np.mean(sentence_lengths), 'sentence_length_std_dev': np.std(sentence_lengths) })

    def word_richness(self):
        self.row.update( {'word_richness': len(self.tokens) / len(set(self.tokens)) } )

    def num_sentences(self):
        self.row.update( {'number_sentences': len(self.sentences)} )
