import os
import re

max_number_of_lines = 10000
path = "../texts_stripped/"
new_path = "../texts_cleaned/"
for author_folder in os.listdir(path):
    for file in os.listdir(path + author_folder):
        txt = open(path + author_folder + '/' + file, 'r', errors='ignore').read()
        cleaned = re.sub(r"([A-Za-z.,;:!\'\"\{\}\[\]\(\)&~<>? ])\-([A-Za-z.,;!:\'\"\{\}\[\]\(\)&~<>? ])", r"\1 \2", txt , 0, re.IGNORECASE)
        cleaned = re.sub(r"([A-Za-z.,;:!\'\"\{\}\[\]\(\)&~<>? ])\-\-([A-Za-z.,;!:\'\"\{\}\[\]\(\)&~<>? ])", r"\1 \2", cleaned , 0, re.IGNORECASE)
        cleaned = re.sub(r"([A-Za-z.,;:!\'\"\{\}\[\]\(\)&~<>? ])\-", r"\1 ", cleaned , 0, re.IGNORECASE)
        cleaned = re.sub(r"([A-Za-z.,;:!\'\"\{\}\[\]\(\)&~<>? ])\-\-", r"\1 ", cleaned , 0, re.IGNORECASE)

        #cleaned = re.sub(r"([a-z])\-\-([a-z])", r"\1 \2", txt , 0, re.IGNORECASE)
        directory = new_path + author_folder
        if not os.path.exists(directory):
            os.makedirs( directory )
        f = open(directory + '/' + file, "w+")
        f.write(cleaned)
        f.close()
