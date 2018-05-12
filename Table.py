import pandas as pd
from text_features import Text
import os

class Table():

    def __init__(self, authors):
        path = "data/texts_cleaned/"
        self.authors = authors
        self.pos_grams_table = pd.DataFrame()
        self.n_grams_table = pd.DataFrame()
        self.stylometry_table = pd.DataFrame()

        for author in self.authors:
            print(author)
            for book in os.listdir(path + '/' + author):
                print(book)
                text = Text( open(path + '/' + author + '/' + book, 'r', errors='ignore').read(), author )
                print('text retrieved')
                self.pos_grams_table = self.pos_grams_table.append( pd.DataFrame( text.pos_gram_data(), index=[book] ) )
                print('pos')
                self.n_grams_table = self.n_grams_table.append( pd.DataFrame( text.word_gram_data(), index=[book] ) )
                print('ngrams')
                self.stylometry_table = self.stylometry_table.append( pd.DataFrame( text.stylometric_data(), index=[book] ) )
                print('stylometry')

            self.pos_grams_table["author"]=author
            self.n_grams_table["author"]=author
            self.stylometry_table["author"]=author


        self.eliminate_non_significant_columns(self.pos_grams_table, 0.01)
        self.eliminate_non_significant_columns(self.n_grams_table, 0.01)

        self.merge_frames()


    def eliminate_sparse_columns(self, frame, threshold): # threshold -> min_percent_data
        pass



    def eliminate_non_significant_columns(self):
        for column in frame:
            # frame[column]
            means = []
            stds = []
            for author in self.authors:
                sub_frame = frame.loc[frame['author'] == author]
                means.append( sub_frame.mean() )
                stds.append( sub_frame.std() )
            print(np.mean( stds ))
            print(np.std( means ))
            



if __name__ == '__main__':
    authors = ['jane_austen', 'charles_dickens']
    table = Table(authors)
