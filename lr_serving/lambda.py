import time
import psutil
import os
pid = os.getpid()
python_process = psutil.Process(pid)
memoryUse_old = 0
time1 = time.time()
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
import os
import re

memoryUse = python_process.memory_info()[0]/2.**30
print('memory use 1:', memoryUse-memoryUse_old)
time2 = time.time()

cleanup_re = re.compile('[^a-z]+')

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

dataset = pd.read_csv('/home/jovans2/apps/lr_serving/dataset.csv')
df_input = pd.DataFrame()
dataset['train'] = dataset['Text'].apply(cleanup)
tfidf_vect = TfidfVectorizer(min_df=100).fit(dataset['train'])
x = 'The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.  '
df_input['x'] = [x]
df_input['x'] = df_input['x'].apply(cleanup)
X = tfidf_vect.transform(df_input['x'])

x = 'My favorite cafe. I like going there on weekends, always taking a cafe and some of their pastry before visiting my parents.  '
df_input['x'] = [x]
df_input['x'] = df_input['x'].apply(cleanup)
X2 = tfidf_vect.transform(df_input['x'])

model = joblib.load('/home/jovans2/apps/lr_serving/lr_model.pk')
print('Model is ready')
time3 = time.time()
memoryUse_old = memoryUse
memoryUse = python_process.memory_info()[0]/2.**30
print('memory use 2:', memoryUse-memoryUse_old)

def main(params):
    y = model.predict(X)
    print(y)
    time4 = time.time()
    print(time2-time1)
    print(time3-time2)
    print(time4-time3)
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30
    print('memory use 3:', memoryUse-memoryUse_old)

    return y