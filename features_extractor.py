import pandas as pd
import os
import text_features
import random
class Text_Features_df():
    def __init__(self, author):
        self.df = self.build_df(author)
    def build_df(self, author):
        books_df = pd.DataFrame()

        #authors = ['lewis_carroll']

        path = "./data/texts_cleaned/" + author
        books = os.listdir(path)
        if '.DS_Store' in books:
            books.remove('.DS_Store')
        num = 15
        random_int = random.sample(range(0,len(books)), num)
        for i in random_int:
            if books[i] == '.DS_Store':
                continue
            book_path = path + "/" + books[i]
            with open(book_path, encoding="utf8", errors='ignore') as f:
                contents = f.read()
            text = text_features.Text(contents, author)
            book_df = pd.DataFrame(text.row,index =[books[i]])
            books_df = books_df.append(book_df)
            print(books_df.shape,": ",books[i])

        books_df = books_df.fillna(0)
        return process(books_df, 0.15, 0.85)

def process(books_df, lower_bound, upper_bound):
    sum = books_df.std(numeric_only=True)
    sum = sum.sort_values()
    not_ngrams = ['word_length_std_dev','word_length_avg','sentence_length_std_dev','word_richness','sentence_length_avg','number_sentences']
    for n in not_ngrams:
        del sum[n]
    lower = sum.quantile(q=lower_bound)
    upper = sum.quantile(q=upper_bound)
    del_col = sum[sum <= lower].append( sum[sum >= upper])
    keys = del_col.keys()
    for k in keys:
        print(k)
        del  books_df[k]
    return books_df


def combine_author_df(authors):
    author_dfs = []
    for author in authors:
        print(author)
        author_df = Text_Features_df(author)
        author_dfs.append(author_df.df)
    books_df = pd.concat(author_dfs)
    books_df = books_df.fillna(0)
    print(books_df.shape)
    books_df.to_csv("3author_both_3grams.csv", sep='\t', encoding='utf-8')


def main():
    authors = ['mark_twain','mildred_a._wirt','oscar_wilde']
    #authors = ['test1','test2']
    combine_author_df(authors)
    #books_df = pd.read_csv('./3author_both_3grams.csv', sep='\t')
    #print(books_df.shape)
    books_df = pd.read_csv('./3author_both_3grams.csv', sep='\t')
    process_df = process(books_df, 0.25, 0.75)
    process_df.to_csv("3author_both_3grams_processed.csv", sep='\t', encoding='utf-8')


if __name__ == "__main__":
    main()
