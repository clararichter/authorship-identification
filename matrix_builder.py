import pandas as pd
from text_features import Text
import os
import csv
import numpy as np

class Matrix():

    def __init__(self, authors):
        path = "data/texts_cleaned"
        self.matrix = pd.DataFrame()
        self.authors = authors
        self.build_matrix(path)


    def build_matrix(self, path):
        books = []
        index = []
        for author in self.authors:
            print(author)
            for book in os.listdir(path + '/' + author):
                print("\t", book)
                text = Text( open(path + '/' + author + '/' + book, 'r', errors='ignore').read(), author )
                # book = text.vector
                # print(book)
                books.append(text.vector)
                index.append(book)
                #self.matrix = self.matrix.append( pd.DataFrame(text.get_vector(), index=[book] ) )
        self.matrix = pd.DataFrame.from_records(books, index = index)

        print("features retrieved")
        self.matrix = self.matrix.fillna(0)
        #self.matrix.to_csv("4author2grams.csv", encoding='utf-8')
        self.eliminate_sparse_columns(.5)
        self.matrix.to_csv("10author1grams_post_sparcity.csv", encoding='utf-8')
        self.eliminate_non_significant_columns(.3)
        self.matrix.to_csv("10author1grams.csv", encoding='utf-8')



    def eliminate_sparse_columns(self, threshold): # threshold -> min_percent_data
        # print("starting csv read")
        # self.matrix = pd.read_csv("./matrix_builder_full_table.csv", header=0, index_col=0)

        print("eliminate_sparce_columns_function")
        columns_to_keep = ['original_book_author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        feature_list = list( set(self.matrix.columns.values).difference( set( columns_to_keep ) ) )
        sparcity_data = pd.DataFrame(columns=self.authors, index=feature_list)

        for author in self.authors:
            print("\t", author)
            subframe = self.matrix.loc[self.matrix['original_book_author'] == author]
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
        # print("starting csv read")
        # self.matrix = pd.read_csv("./matrix_builder_post_sparcity.csv", header=0, index_col=0)

        print('eliminate_non_significant_columns function')
        # Columns we want to avoid
        columns_to_keep = ['original_book_author', 'word_length_avg', 'word_length_std_dev', 'sentence_length_avg', 'sentence_length_std_dev', 'word_richness']
        # Make two tables for the means and std's by authors
        feature_list = list( set(self.matrix.columns.values).difference( set( columns_to_keep ) ) )
        mean_feature_data = pd.DataFrame(columns=self.authors, index=feature_list)
        std_feature_data = pd.DataFrame(columns=self.authors, index=feature_list)

        feature_data = pd.DataFrame(columns=['mean_of_stds','std_of_means'], index=feature_list)

        for author in self.authors:
            print("\t", author)
            subframe = self.matrix.loc[self.matrix['original_book_author'] == author]
            for column in subframe:
                if column not in columns_to_keep:
                    mean_feature_data.at[column, author] = np.mean(subframe[column])
                    std_feature_data.at[column, author] = np.std(subframe[column])

        print("\tsub tables built, constructing feature table")
        for column in feature_list:
            feature_data.at[column,'mean_of_stds'] = np.mean(std_feature_data.loc[column])
            feature_data.at[column,'std_of_means'] = np.mean(mean_feature_data.loc[column])

        print("\tdrops")
        drops = feature_data.sort_values(by=['mean_of_stds']).head( int(threshold * feature_data.shape[0]))
        self.matrix = self.matrix.drop( drops.index, axis=1 )
        drops = feature_data.sort_values(by=['std_of_means']).tail( int(threshold * feature_data.shape[1]))
        self.matrix = self.matrix.drop( drops.index, axis=1 )

if __name__ == '__main__':
    matrix = Matrix(['mildred_a._wirt','oscar_wilde', 'mark_twain', 'elizabeth_gaskell', "george_eliot", "thomas_hardy", "robert_louis_stevenson", "arthur_conan_doyle", "edgar_rice_burroughs", "jack_london"])
