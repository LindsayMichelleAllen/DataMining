import logging
import io

### Create the logger
logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)

### Setup the console handler with a StringIO object
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

### Optionally add a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

### Add the console handler to the logger
logger.addHandler(ch)



import pandas as pd
import numpy as np
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

stop = stopwords.words('english')

x = pd.read_csv('traindata.txt', header=None)
y = pd.read_csv('trainlabels.txt', header=None)
z = pd.read_csv('stoplist.txt', header=None)
predData = pd.read_csv('testdata.txt', header=None)
predLabels = pd.read_csv('testlabels.txt', header=None)

# Train Data Size
rangeX = x.size
rangePred = predData.size

# Rename Columns
x.columns = ['Data']
y.columns = ['Label']
z.columns = ['Stop']
predData.columns = ['Data']
predLabels.columns = ['Label']

# Combining Train and Test
dx = pd.concat([x, predData])

# List of Stop Words
stopwords = z['Stop'].tolist()

# Creating Tokenized Data
dx['Filt_Data'] = dx['Data'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
del dx['Data']
dx['Tokenized_Data'] = dx.apply(lambda row: nltk.word_tokenize(row['Filt_Data']), axis=1)

# Train Labels to List
y = y['Label'].tolist()
# Test Labels to List
predLabels = predLabels['Label'].tolist()

# Training Data
v = TfidfVectorizer()

Tfidf = v.fit_transform(dx['Filt_Data'])

df1 = pd.DataFrame(Tfidf.toarray(), columns=v.get_feature_names())
print(df1)

#Separating Train and Test
x = df1[0:rangeX]
predData = df1[rangeX:rangeX+rangePred]

# Perceptron Implementation
logger.debug(str(Perceptron(max_iter=20, eta0=1, random_state=0, verbose=1)))
# Fitting x, y
ppn = Perceptron(max_iter=20, eta0=1, random_state=0, verbose=1)
ppn.fit(x,y)

# Using Test Data
y_pred = ppn.predict(predData)

# Accuracy Calculation
print('Accuracy %.2f' % accuracy_score(predLabels, y_pred))

### Pull the contents back into a string and close the stream
log_contents = log_capture_string.getvalue()
log_capture_string.close()

### Output as lower case to prove it worked. 
print(log_contents)