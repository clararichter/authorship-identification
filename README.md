# Authorship Identification Machine Learning Model

This repository represents our concerted effort to create a machine learning model that identifies what author 
among 10 candidates wrote a given excerpt of text. It includes a data 
pipeline, consisting of web scraping retrieval, basic natural language data processing, as well as the 
construction of a supervised 
classification model. The model uses stylometric features -- quantifiable features that 
capture some element of a work's style -- to perform the classification. Using the modeling techniques of 
Logistic Regression and Support Vector Machines and k-fold cross validation, the models 
achieved an accuracy 
ranging from 90% to 8% depending on the number of candidate authors being classified as well as the number of 
style feature traits trained on.

The authors for whom we have created the model are all English authors of classic works--Mildred A. Wirt, Oscar 
Wilde, Mark Twain, Elizabeth Gaskell, 
George Eliot, Thomas Hardy, Robert Louis Stevenson, Arthur Conan Doyle, Edgar Rice Burroughs, Jack London. 
With little effort it should be possible to contruct a model for a different set of authors, as long as relevant texts 
are available at Gutenberg.org, which is the source from where we retrieved the raw data.

### Prerequisites

The project is based on Python 3, and dependencies can be installed through the [Anaconda Software Package]
(https://www.anaconda.com/download/#macos). It is also uses dependencies from the [Natrual Language Took Kit]
(https://www.nltk
.org/install.html).
