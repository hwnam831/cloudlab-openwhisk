import json
import random

trainset0 = ['ocr-img', 'ml_trainnig', 'cnn_serving', 'base64']
trainset1 = ['matmul', 'rnn_serving',  'video_processing', 'img_rotate']
valset0 = ['linpack', 'img-resize']
valset1 = ['lr_serving', 'primes']

def create_json(name1, name2):
    base_json = {"test_duration_in_seconds": 90,
    "blocking_cli": false}
    base_json["random_seed"] = random.randint(0,100)
    base_json["test_name"] = name1 + "_" + name2
    base_json["instances"] = {}
    json1 = json.

if __name__=='__main__':
