from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import re
from nltk.corpus import stopwords
from bs4 import BeautifulSoup




def get_input(filename):
    """
        Read the Testing File
    """
    fp = pd.read_csv(filename)
    return fp

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

# read csv
trainingSet = pd.read_csv('./Training_Merged.csv')

# give testing file parameter
testingSet = get_input('./testing.csv')

# shuffle data across csv
trainingSet = shuffle(trainingSet)

# removing unwanted characters
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

# passing to function
trainingSet['Description'] = trainingSet['Description'].apply(clean_text)
testingSet['Description'] = testingSet['Description'].apply(clean_text)

# remove NA values
trainingSet.dropna()
testingSet.dropna()

# Choose dependent and independent variables
X_train = trainingSet.Description
y_train = trainingSet.Title

# Testing Data Should have header name as "Description"
X_test = testingSet.Description

# Spilt data into training and testing
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

# Build a counter based on the training dataset
counter = CountVectorizer()
counter.fit(X_train)

# count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(X_train) # transform the training data

counts_test = counter.transform(X_test) # transform the testing data

# train classifier
model_1 = DecisionTreeClassifier()
model_2 = MultinomialNB()
model_3= LogisticRegression(solver='liblinear')
model_4= RandomForestClassifier(n_estimators=2500, n_jobs=-1,criterion="entropy",max_features='auto',random_state=150,max_depth=1000,min_samples_split=160 )
#model5 = MLPClassifier( hidden_layer_sizes=(15,), random_state=1, max_iter=13, warm_start=True)
#model6 = MLPClassifier()

predictors=[('dt',model_1), ('mnb',model_2), ('lr', model_3), ('rfc', model_4)]

# Pass all predictors to Voting Classifier
VT=VotingClassifier(predictors)

# train all classifier on the same datasets
VT.fit(counts_train,y_train)

# use hard voting to predict (majority voting)
pred=VT.predict(counts_test)

# Output the predicted job title to a new file
output = pd.DataFrame()
output['Predicted Job Title'] = pred
output.to_csv('Final_Output.csv')



################################################################################

# LDA

# from sklearn.metrics import accuracy_score
# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.feature_extraction.text import CountVectorizer
# import os, glob

# def getInput(filename):
#     fname = pd.read_csv(os.path.join(os.getcwd(), filename))
#     fname = fname.dropna(axis= 0)
#     return fname

# #test_df = getInput('test.csv')
# combined_dataset = getInput('E:\\Stevens Institute of Technology\\3rd Sem\\BIA-660\\Project\\Merged.csv')
# combined_dataset.dropna()
# #LDA machine learning to predict JobTitle
# count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')

# #The dataset should have two columns COL_1: JOB-TITLE, COL_2: DESCRIPTION
# doc_term_matrix = count_vect.fit_transform(combined_dataset['Description'])
# LDA=LatentDirichletAllocation(n_components=3,random_state=42)
# LDA.fit(doc_term_matrix)
# topic_values=LDA.transform(doc_term_matrix)
# combined_dataset['Predicted-Job-Title']=topic_values.argmax(axis=1)

# #print(combined_dataset.to_csv('Result.csv'))
# def r(topic):
#     if topic==0:
#         return 'Data Scientist'
#     elif topic==1:
#         return 'Data Engineer'
#     elif topic==2:
#         return 'Software Engineer'

# combined_dataset['Predidcted_Title']=combined_dataset['Predicted-Job-Title'].apply(r)
# combined_dataset.to_csv("Final_Output.csv")


