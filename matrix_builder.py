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

        self.matrix = self.matrix.fillna(0)
        print("writing csv")
        self.matrix.to_csv("pre_processed_all_features_austen.csv", encoding="utf-8")
        print("eliminate_sparse_columns")
        self.eliminate_sparse_columns(.5)
        print("non_significant")
        self.eliminate_non_significant_columns(.3)

        self.matrix.to_csv("booksyay.csv", encoding='utf-8')



    def eliminate_sparse_columns(self, threshold): # threshold -> min_percent_data

        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        sparcity_data = pd.DataFrame(columns=self.authors, index=list(self.matrix.columns.values))

        for author in self.authors:
            print(author)
            print(self.matrix['author'] )
            subframe = self.matrix.loc[self.matrix['author'] == author]
            for column in subframe:
                if column not in columns_to_keep:
                    subcolumn = subframe[column]
                    number_of_zeros = (subcolumn == 0).sum()
                    percent_data = (len(subcolumn) - number_of_zeros) / len(subcolumn)
                    sparcity_data.at[column, author] = percent_data

        sparcity_data = pd.DataFrame(data=sparcity_data.min(axis=1), columns=['min'])
        sparcity_data = sparcity_data[sparcity_data['min'] >= threshold]
        self.matrix = self.matrix.drop( sparcity_data.index, axis=1 )



    def old_eliminate_non_significant_columns(self, threshold):
        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        feature_data = pd.DataFrame(columns=['mean_of_stds','std_of_means'])

        for column in self.matrix:
            if column not in columns_to_keep:
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


    def eliminate_non_significant_columns(self, threshold):
        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        mean_feature_data = pd.DataFrame(columns=self.authors, index=list(self.matrix.columns.values))
        std_feature_data = pd.DataFrame(columns=self.authors, index=list(self.matrix.columns.values))
        feature_data = pd.DataFrame(columns=['mean_of_stds','std_of_means'], index=list(self.matrix.columns.values))
        for author in self.authors:
            subframe = self.matrix.loc[self.matrix['author'] == author]
            for column in subframe:
                if column not in columns_to_keep:
                    mean_feature_data.at[column, author] = np.mean(subframe[column])
                    std_feature_data.at[column, author] = np.std(subframe[column])

        for column in self.matrix.columns.values:
            feature_data.at[column,'mean_of_stds'] = np.mean(std_feature_data[column])
            feature_data.at[column,'mean_of_stds'] = np.mean(mean_feature_data[column])


        feature_data = feature_data.sort_values(by=['mean_of_stds']).head( int(threshold * self.matrix.shape[1]))
        self.matrix = self.matrix.drop( feature_data.index, axis=1 )
        feature_data = feature_data.sort_values(by=['std_of_means']).tail( int(threshold * self.matrix.shape[1]))
        self.matrix = self.matrix.drop( feature_data.index, axis=1 )

if __name__ == '__main__':
    matrix = Matrix(['jane_austen'])
