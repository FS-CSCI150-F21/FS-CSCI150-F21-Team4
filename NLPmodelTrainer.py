import csv
import numpy as np
import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

features = []
labels = []

with open("training.1600000.processed.noemoticon.csv", mode='r') as csvOut:
    outfile = csv.reader(csvOut, delimiter=',')
    initialLine = True
    for row in outfile:
        if initialLine == False:
            initialLine = True
        else:
            features.append(row[5])
            labels.append(row[0])

processed_features = []
valRange = 1
numFeatStart = int(len(features)* (.5-valRange/2))
numFeatEnd = int(len(features)* (.5+valRange/2))
scaleLabel = labels[numFeatStart:numFeatEnd]

for sentence in range(numFeatStart, numFeatEnd):
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(features[sentence]))

    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

    # Substituting multiple spaces with single space
    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)

    # Converting to Lowercase
    processed_feature = processed_feature.lower()

    processed_features.append(processed_feature)

print("Finished Text Processing")
vectorizer = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
processed_features = vectorizer.fit_transform(processed_features).toarray()
with open("vectorizer.pickle", "wb") as pickle_out:
    pickle.dump(vectorizer, pickle_out)
print(processed_features.shape)
print("Splitting Tests")
X_train, X_test, y_train, y_test = train_test_split(processed_features, scaleLabel, test_size=0.2, random_state=0)

print("Fitting Logistic Regression")
text_classifier = LogisticRegression(random_state=0)
text_classifier.fit(X_train, y_train)
with open("LogisticRegClass.pickle", "wb") as pickle_out:
    pickle.dump(text_classifier, pickle_out)
print("Fitting Completed")
