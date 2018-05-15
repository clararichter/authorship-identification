import pandas as pd
import os
import text_features


def build_author_df( author, books = None):
    books_df = pd.DataFrame()

    #authors = ['lewis_carroll']

    path = "./data/texts_cleaned/" + author
    if books == None:
        books = os.listdir(path)
        if '.DS_Store' in books:
            books.remove('.DS_Store')

    if len(books) == 1:
        book_path = path + "/" + books[0]
        with open(book_path, encoding="utf8", errors='ignore') as f:
            contents = f.read()
        text = text_features.Text(contents, author)
        book_df = pd.DataFrame(text.row,index =[books[0]])
        print(book_df.shape,": ",books[0])
        return book_df
    mid = len(books)// 2
    combined = pd.concat([build_author_df(author, books[:mid]), build_author_df(author, books[mid:])])
    return combined

    # for book in books:
    #     if book == '.DS_Store':
    #         continue
    #     book_path = path + "/" + book
    #     with open(book_path, encoding="utf8", errors='ignore') as f:
    #         contents = f.read()
    #     text = text_features.Text(contents, author)
    #     book_df = pd.DataFrame(text.row,index =[book])
    #     books_df = books_df.append(book_df)
    #     print(books_df.shape,": ",book)
    # return books_df

def process():
    books_df = pd.read_csv('./3author_recursion.csv')
    sum = books_df.std(numeric_only=True)
    sum = sum.sort_values()
    not_ngrams = ['word_length_std_dev','word_length_avg','sentence_length_std_dev','word_richness','sentence_length_avg','number_sentences']
    for n in not_ngrams:
        del sum[n]
    lower = sum.quantile(q=0.20)
    upper = sum.quantile(q=0.80)
    del_col = sum[sum <= lower].append( sum[sum >= upper])
    keys = del_col.keys()
    for k in keys:
        print(k)
        del  books_df[k]
    books_df.to_csv("3author_recursion_processed.csv", sep='\t', encoding='utf-8')

def combine_author_df(authors):
    author_dfs = []
    for author in authors:
        print(author)
        author_df = build_author_df(author=author)
        print(author_df.shape)
        author_dfs.append(author_df)
    books_df = pd.concat(author_dfs)
    books_df = books_df.fillna(0)
    print(books_df.shape)
    books_df.to_csv("3author_recursion.csv", sep='\t', encoding='utf-8')


def main():
    authors = ['mark_twain','mildred_a._wirt','oscar_wilde']
    #authors = ['test1','test2']
    combine_author_df(authors)



if __name__ == "__main__":
    main()
