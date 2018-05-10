import pandas as pd
import os
import text_features

def build_csv():
    books_df = pd.DataFrame()
    #authors = ['mark_twain','mildred_a._wirt','oscar_wilde']
    authors = ['lewis_carroll']
    for author in authors:
        path = "./data/texts_cleaned/" + author
        books = os.listdir(path)

        for i in range(0, len(books)):
            if books[i] == '.DS_Store':
                continue
            book_path = path + "/" + books[i]
            with open(book_path, encoding="utf8", errors='ignore') as f:
                contents = f.read()
            #encoding='utf-8'
            text = text_features.Text(contents, author)

            #text = text_features.Text(open(path + "/" + books[i],'r').read(), author)
            print('1', text.row['textbook_author*'])
            book_df = pd.DataFrame(text.row,index =[books[i]])
            print('2', text.row['textbook_author*'])
            books_df = books_df.append(book_df)
            print('3', text.row['textbook_author*'])

            print(books_df.shape,": ",books[i])
    books_df = books_df.fillna(0)
    books_df.to_csv("test.csv", sep='\t', encoding='utf-8')
    #
    #print(sum.quantile(q=0.25))
    # with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    #     print(sum)

def process():
    books_df = pd.read_csv('./3books.csv')
    sum = books_df.sum(numeric_only=True)
    sum = sum.sort_values()
    not_ngrams = ['word_length_std_dev','word_length_avg','sentence_length_std_dev','word_richness','sentence_length_avg','number_sentences']
    for n in not_ngrams:
        del sum[n]
    #print(sum)
    lower = sum.quantile(q=0.15)
    upper = sum.quantile(q=0.85)

    del_col = sum[sum <= lower].append( sum[sum >= upper])

    keys = del_col.keys()
    #print(len(keys))


    #print(books_df.shape)
    for k in keys:
        print(k)
        del  books_df[k]
    #print(books_df.shape)
    print(books_df['author'])
    books_df.to_csv("3books_processed.csv", sep=',', encoding='utf-8')


    #print(lower, upper)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    #      print(sum)



def check():
    books_df = pd.read_csv('./test.csv',sep='\t')
    print(books_df['textbook_author*'])

build_csv()
#process()
#check()
