import sklearn
import numpy as np
import pandas as pd 
import pickle

data = pd.read_csv('https://raw.githubusercontent.com/FS-CSCI150-F21/FS-CSCI150-F21-Team4/main/datasets/train.csv')
data = data.drop(columns=['textID', 'selected_text'])

data = data.dropna()
training_data = data

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
text_clf = Pipeline([
  ('vect', CountVectorizer()),
  ('tfidf', TfidfTransformer()),
  ('clf', CalibratedClassifierCV(LinearSVC(loss='hinge', max_iter=2000, C=0.8))),
])

test_data = pd.read_csv('https://raw.githubusercontent.com/FS-CSCI150-F21/FS-CSCI150-F21-Team4/main/datasets/test.csv')
test_data = test_data.drop(columns=['textID'])

text_clf.fit(training_data.text, training_data.sentiment)
predicted = text_clf.predict(test_data.text)
print(np.mean(predicted == test_data.sentiment))

filename = 'svm_model.sav'
pickle.dump(text_clf, open(filename, 'wb'))