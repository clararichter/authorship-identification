import nltk
from nltk.util import ngrams
from nltk import word_tokenize
import operator

def get_vector(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    map =  {}
    for n in range(2, 3):
        map.update( get_ngram_vector(tokens, n) )
    return map


def get_ngram_vector(tokens, n):
    grams = ngrams(tokens, n)
    (gram_map, total_number_of_grams) = get_gram_map(grams)
    for ( gram, count ) in gram_map.items():
        gram_map[gram] = ( count, count / total_number_of_grams )
    return gram_map


def get_gram_map(grams):
    gram_map = {}
    counter = 0
    for gram in grams:
        counter+=1
        if gram in gram_map:
            gram_map[gram] += 1
        else:
            gram_map[gram] = 1
    return gram_map, counter


def main():
    file = open("books/oliver_twist_730.txt",'r')
    text = file.read()
    vector = get_vector(text)
    print(vector)

if __name__ == '__main__':
    main()
