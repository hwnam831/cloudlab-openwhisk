import time
import psutil
import os
pid = os.getpid()
python_process = psutil.Process(pid)
memoryUse_old = 0
t1 = time.time()
import os
from minio import Minio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import re
memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
print('memory use 1:', memoryUse-memoryUse_old)
t2 = time.time()
cleanup_re = re.compile('[^a-z]+')

responses = ["record_response", "replay_response"]

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

df_name = 'reviews10mb.csv'
df2_name = 'dataset2.csv'
df_path = 'amzn_fine_food_reviews/' + df_name
df2_path = 'pulled_' + df2_name

def getMinioClient(access, secret):
    return Minio(
        '10.10.1.1:9000',
        access_key = access,
        secret_key = secret,
        secure = False
    )

minioClient = getMinioClient("minioadmin", "minioadmin")

minioClient.fget_object('testbucket', df_path, df_name)

df = pd.read_csv(df_path)
df['train'] = df['Text'].apply(cleanup)

t3 = time.time()

def main(params):
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 2:', memoryUse-memoryUse_old)

    model = LogisticRegression()
    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])
    train = tfidf_vector.transform(df['train'])
    model.fit(train, df['Score'])

    t4 = time.time()
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 3:', memoryUse-memoryUse_old)

    return {"Ok":"done"}
