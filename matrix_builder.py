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
            for book in os.listdir(path + '/' + author):
                text = Text( open(path + '/' + author + '/' + book, 'r', errors='ignore').read(), author )
                self.matrix = self.matrix.append( pd.DataFrame(text.get_vector(), index=[book] ) )

        self.matrix = self.matrix.fillna(0)
        self.eliminate_sparse_columns(.5)
        self.eliminate_non_significant_columns(.3)
        self.matrix.to_csv("booksyay.csv", encoding='utf-8')



    def eliminate_sparse_columns(self, threshold): # threshold -> min_percent_data

        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        feature_list = list( set(self.matrix.columns.values).difference( set( columns_to_keep ) ) )
        sparcity_data = pd.DataFrame(columns=self.authors, index=feature_list)

        for author in self.authors:
            subframe = self.matrix.loc[self.matrix['author'] == author]
            for column in subframe:
                if column not in columns_to_keep:
                    subcolumn = subframe[column]
                    number_of_zeros = (subcolumn == 0).sum()
                    percent_data = (len(subcolumn) - number_of_zeros) / len(subcolumn)
                    sparcity_data.at[column, author] = percent_data

        sparcity_data = pd.DataFrame(data=sparcity_data.min(axis=1), columns=['min'])
        sparcity_data = sparcity_data[sparcity_data['min'] <= threshold]
        self.matrix = self.matrix.drop( sparcity_data.index, axis=1 )



    def eliminate_non_significant_columns(self, threshold):
        print('eliminate signifcant')
        # Columns we want to avoid
        columns_to_keep = ['author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        # Make two tables for the means and std's by authors
        feature_list = list( set(self.matrix.columns.values).difference( set( columns_to_keep ) ) )
        mean_feature_data = pd.DataFrame(columns=self.authors, index=feature_list)
        std_feature_data = pd.DataFrame(columns=self.authors, index=feature_list)

        feature_data = pd.DataFrame(columns=['mean_of_stds','std_of_means'], index=feature_list)

        for author in self.authors:
            print('jane autsten')
            subframe = self.matrix.loc[self.matrix['author'] == author]
            for column in subframe:
                if column not in columns_to_keep:
                    mean_feature_data.at[column, author] = np.mean(subframe[column])
                    std_feature_data.at[column, author] = np.std(subframe[column])

        for column in feature_list:
            print(column)
            feature_data.at[column,'mean_of_stds'] = np.mean(std_feature_data.loc[column])
            feature_data.at[column,'std_of_means'] = np.mean(mean_feature_data.loc[column])


        drops = feature_data.sort_values(by=['mean_of_stds']).head( int(threshold * feature_data.shape[0]))
        self.matrix = self.matrix.drop( feature_data.index, axis=1 )
        drops = feature_data.sort_values(by=['std_of_means']).tail( int(threshold * feature_data.shape[1]))
        self.matrix = self.matrix.drop( feature_data.index, axis=1 )

if __name__ == '__main__':
    matrix = Matrix(['jane_austen'])
