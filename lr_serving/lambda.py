import time
import psutil
import os

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
import os
import re
from minio import Minio

def cleanup(sentence):
    cleanup_re = re.compile('[^a-z]+')
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

def getMinioClient(access, secret):
    return Minio(
        '10.10.1.1:9000',
        access_key = access,
        secret_key = secret,
        secure = False
    )

def main(params):
    pid = os.getpid()
    python_process = psutil.Process(pid)
    memoryUse_old = 0
    time1 = time.time()
    memoryUse = python_process.memory_info()[0]/2.**30
    print('memory use 1:', memoryUse-memoryUse_old)
    time2 = time.time()

    datafile='reviews50mb.csv'

    minioClient = getMinioClient("minioadmin", "minioadmin")

    minioClient.fget_object('testbucket', 'amzn_fine_food_reviews/'+datafile, '/tmp/'+datafile)

    dataset = pd.read_csv('/tmp/'+datafile)
    df_input = pd.DataFrame()
    dataset['train'] = dataset['Text'].apply(cleanup)
    tfidf_vect = TfidfVectorizer(min_df=100,max_features=2338).fit(dataset['train'])
    x = 'The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.'
    df_input['x'] = [x]
    df_input['x'] = df_input['x'].apply(cleanup)
    X = tfidf_vect.transform(df_input['x'])

    #x = 'My favorite cafe. I like going there on weekends, always taking a cafe and some of their pastry before visiting my parents.  '
    #df_input['x'] = [x]
    #df_input['x'] = df_input['x'].apply(cleanup)
    #X2 = tfidf_vect.transform(df_input['x'])
    minioClient.fget_object('testbucket', 'model/lr_model.pk', '/tmp/lr_model.pk')
    model = joblib.load('/tmp/lr_model.pk')
    print('Model is ready')
    time3 = time.time()
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30
    print('memory use 2:', memoryUse-memoryUse_old) 
    y = model.predict(X)
    print(y)
    time4 = time.time()
    print(time2-time1)
    print(time3-time2)
    print(time4-time3)
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30
    print('memory use 3:', memoryUse-memoryUse_old)

    return {'prediction':str(y), 'time':time4-time1}