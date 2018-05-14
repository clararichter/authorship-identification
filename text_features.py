from nltk.util import ngrams
from nltk.tokenize import TweetTokenizer, sent_tokenize
import numpy as np
import nltk
import collections

class Text():

    def __init__(self, text, author):
        self.author = author
        self.text = text.lower()
        self.tokens = TweetTokenizer().tokenize(self.text)
        self.sentences = sent_tokenize(self.text)
        self.total_number_of_tokens = len(self.tokens)
        self.max_ngrams = 3

    def get_vector(self):
        vector = {}
        vector.update( {'original_book_author': self.author } )
        vector.update( self.word_gram_data() )
        vector.update( self.pos_gram_data() )
        vector.update( self.stylometric_data() )
        return vector

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

    def word_gram_data(self):
        output_dictionary = {}
        for n in range(1, self.max_ngrams + 1):
            n_grams = ngrams(self.tokens, n)
            all_grams = list(n_grams)
            total = len(all_grams)
            grams_collection = collections.Counter(all_grams)
            grams_collection = dict(grams_collection)

            for ngram, count in grams_collection.items():
                output_dictionary[" ".join(ngram)] = count/total

        return output_dictionary

    def pos_gram_data(self):
        output_dictionary = {}
        pos_tags = nltk.pos_tag(self.tokens)
        pos_tags = [pos[1] for pos in pos_tags]

        for n in range(1, self.max_ngrams + 1):
            n_grams = ngrams(pos_tags, n)
            all_grams = list(n_grams)
            total = len(all_grams)
            grams_collection = collections.Counter(all_grams)
            grams_collection = dict(grams_collection)

            for ngram, count in grams_collection.items():
                output_dictionary[" ".join(ngram)] = count/total

        return output_dictionary

    def word_lengths(self):
        word_lengths = []
        forbidden = [".", ",", "?", "!", "\"","\'",";",":"]
        for word in self.tokens:
            if word not in forbidden:
                word_lengths.append(len(word))
        return sorted(word_lengths)

    def stylometric_data(self):
        output = self.word_length_data()
        output.update(self.sentence_length_data())
        output.update(self.word_richness())
        return output

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
        #self.row.update( {'word_length_avg': np.mean(word_lengths),'word_length_std_dev': np.std(word_lengths)} )
        return ( {'word_length_avg': np.mean(word_lengths),'word_length_std_dev': np.std(word_lengths)} )

    def sentence_length_data(self):
        sentence_lengths = self.sentence_lengths()
        # self.row.update( {'sentence_length_avg': np.mean(sentence_lengths), 'sentence_length_std_dev': np.std(sentence_lengths) })
        return ( {'sentence_length_avg': np.mean(sentence_lengths), 'sentence_length_std_dev': np.std(sentence_lengths) })

    def word_richness(self):
        # self.row.update( {'word_richness': len(self.tokens) / len(set(self.tokens)) } )
        return ( {'word_richness': len(self.tokens) / len(set(self.tokens)) } )

    def num_sentences(self):
        self.row.update( {'number_sentences': len(self.sentences)} )

if __name__ == '__main__':
    pass
