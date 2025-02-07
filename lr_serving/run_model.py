import time

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
import re
import random
import argparse

def cleanup(sentence):
    cleanup_re = re.compile('[^a-z]+')
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


if __name__=='__main__':
    random.seed(17)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workload",
        type=str,
        default="low",
        choices=['low','med','high','random','sinusoidal'],
        help="workload heaviness",
    )
    parser.add_argument(
        "--duration", type=int, default=60, help="Benchmark duration in seconds"
    )
    parser.add_argument(
        "--downloadonly",
        action="store_true"
    )
    args = parser.parse_args()
    time1 = time.time()

    time2 = time.time()

    if args.workload == 'low':
        datafile='/serverless-faas-workbench/dataset/amzn_fine_food_reviews/reviews10mb.csv'
        nfeatures=1279
    elif args.workload == 'med':
        datafile='/serverless-faas-workbench/dataset/amzn_fine_food_reviews/reviews20mb.csv'
        nfeatures=2338
    elif args.workload == 'high':
        datafile='/serverless-faas-workbench/dataset/amzn_fine_food_reviews/reviews50mb.csv'
        nfeatures=2338
    else:
        datafile='/serverless-faas-workbench/dataset/amzn_fine_food_reviews/reviews20mb.csv'
        nfeatures=2338



    dataset = pd.read_csv(datafile)
    df_input = pd.DataFrame()
    dataset['train'] = dataset['Text'].apply(cleanup)
    tfidf_vect = TfidfVectorizer(min_df=100,max_features=nfeatures).fit(dataset['train'])
    model = joblib.load('/serverless-faas-workbench/dataset/model/lr_model.pk')
    print('Model is ready')
    curtime = time.time()
    endtime = curtime + args.duration
    while curtime < endtime:
        x = 'The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.'
        df_input['x'] = [x]
        df_input['x'] = df_input['x'].apply(cleanup)
        X = tfidf_vect.transform(df_input['x'])
        
        y = model.predict(X)
        print(y)
        x = 'My favorite cafe. I like going there on weekends, always taking a cafe and some of their pastry before visiting my parents.  '
        df_input['x'] = [x]
        df_input['x'] = df_input['x'].apply(cleanup)
        X2 = tfidf_vect.transform(df_input['x'])
        y = model.predict(X2)
        print(y)
        curtime = time.time()
