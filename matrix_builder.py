import pandas as pd
from text_features import Text
import os
import csv
import numpy as np

def build_matrix():
    path = "data/texts_cleaned/"
    authors = {'jane_austen':0}
    matrix = pd.DataFrame()

    counter = 0
    for author in authors.keys():
        print(author)
        for book in os.listdir(path + '/' + author):
            if counter < 1:
                print(book)
                text = Text( open(path + '/' + author + '/' + book, 'r', errors='ignore').read(), author )
                matrix = matrix.append( pd.DataFrame(text.get_vector(), index=[book] ))
                counter+=1

    eliminate_sparse_columns(matrix, 0.01)
    eliminate_non_significant_columns(matrix, 0.01, authors)
    matrix = matrix.fillna(0)
    print(matrix.shape)
    matrix.to_csv("booksyay.csv", encoding='utf-8')



def eliminate_sparse_columns(frame, threshold):
    pass



def eliminate_non_significant_columns(matrix, threshold, authors):
    #columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
    columns_to_keep = ['author']

    for column in matrix:
        if column not in columns_to_keep:
            means = []
            stds = []
            for author in authors:
                subcolumn = matrix.loc[matrix['author'] == author][column]
                means.append( np.mean(subcolumn) )
                stds.append( np.std(subcolumn) )

            # print(means )
            # print(stds )
            # print( np.mean(stds) )
            # print( np.std(means) )

            if np.mean(stds) > 2.0:
                # delete column
            if np.std(means) < 2.0:
                # delete column





if __name__ == '__main__':
    build_matrix()
