import os
import re

max_number_of_lines = 10000
path = "../texts_stripped/"
new_path = "../texts_cleaned/"
for author_folder in os.listdir(path):
    for file in os.listdir(path + author_folder):
        txt = open(path + author_folder + '/' + file, 'r').read()
        cleaned = re.sub(r'[—_]+', r' ', txt)
        directory = new_path + author_folder
        if not os.path.exists(directory):
            os.makedirs( directory )
        f = open(directory + '/' + file, "w+")
        f.write(cleaned)
        f.close()
        
