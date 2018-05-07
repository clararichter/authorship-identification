import os

max_number_of_lines = 10000
path = "../texts_stripped/"
new_path = "../texts_split/"
for author_folder in os.listdir(path):
    for file in os.listdir(path + author_folder):
        # os.system( "split -l {} {} {}".format( (max_number_of_lines), (path + author_folder + '/' + file), (new_path + author_folder + '/' + file) ) )
        # quit()
