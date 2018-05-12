import pandas as pd
from text_features import Text
import os
import csv
import numpy as np

class Matrix():

    def __init__(self, authors):
        path = "data/texts_cleaned/"
        self.matrix = pd.DataFrame()
        self.authors = authors
        self.build_matrix(path)


    def build_matrix(self, path):
        for author in self.authors:
            print(author)
            for book in os.listdir(path + '/' + author):
                print(book)
                text = Text( open(path + '/' + author + '/' + book, 'r', errors='ignore').read(), author )
                self.matrix = self.matrix.append( pd.DataFrame(text.get_vector(), index=[book] ) )


        # book = 'the_complete_project_gutenberg_works_of_jane_austen.txt'
        # author = 'jane_austen'
        # text = Text( open(path + '/' + author + '/' + book, 'r', errors='ignore').read(), author )
        # self.matrix = self.matrix.append( pd.DataFrame(text.get_vector(), index=[book] ) )

        self.eliminate_non_significant_columns()
        self.eliminate_sparse_columns()

        self.matrix = self.matrix.fillna(0)
        self.matrix.to_csv("booksyay.csv", encoding='utf-8')



    def eliminate_sparse_columns(self, threshold): # threshold -> min_percent_data

        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        sparcity_data = pd.DataFrame(columns=self.authors, index=list(frame.columns.values))

        for author in self.authors:
            print(author)
            subframe = frame.loc[self.matrix['author'] == author]
            for column in subframe:
                if column not in columns_to_keep:
                    print(column)
                    subcolumn = subframe[column]
                    number_of_zeros = (subcolumn == 0).sum()
                    percent_data = (len(subcolumn) - number_of_zeros) / len(subcolumn)
                    sparcity_data.at[column, author] = percent_data

        sparcity_data = pd.DataFrame(data=sparcity_data.min(axis=1), columns=['min'])
        sparcity_data = sparcity_data[sparcity_data['min'] >= threshold]
        self.matrix = self.matrix.drop( sparcity_data.index, axis=1 )



    def eliminate_non_significant_columns(self, threshold):
        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        feature_data = pd.DataFrame(columns=['mean_of_stds','std_of_means'])

        for column in self.matrix:
            if column not in columns_to_keep:
                print(column)
                means = []
                stds = []
                for author in self.authors:
                    subcolumn = self.matrix.loc[self.matrix['author'] == author][column]
                    means.append( np.mean(subcolumn) )
                    stds.append( np.std(subcolumn) )
                feature_data = feature_data.append( pd.DataFrame( { 'mean_of_stds' : np.mean(stds), 'std_of_means' : np.std(means) }, index=[column] ) )

        feature_data = feature_data.sort_values(by=['mean_of_stds']).head( int(threshold * self.matrix.shape[1]))
        self.matrix = self.matrix.drop( feature_data.index, axis=1 )
        feature_data = feature_data.sort_values(by=['std_of_means']).tail( int(threshold * self.matrix.shape[1]))
        self.matrix = self.matrix.drop( feature_data.index, axis=1 )


if __name__ == '__main__':
    matrix = Matrix(['jane_austen'])
