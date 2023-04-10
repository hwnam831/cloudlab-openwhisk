import json
import random

trainset0 = ['ml_training', 'cnn_serving', 'base64']
trainset1 = ['matmul', 'rnn_serving',  'video_processing', 'image_rotate']
valset0 = ['linpack']
valset1 = ['lr_serving', 'primes']

def create_json(name1, name2):
    base_json = {"test_duration_in_seconds": 90,
    "blocking_cli": False}
    base_json["random_seed"] = random.randint(0,100)
    base_json["test_name"] = name1 + "_" + name2
    base_json["instances"] = {}
    json1 = json.load(open(name1 + '.json','r'))
    json2 = json.load(open(name2 + '.json','r'))
    inst1 = json1["instances"][list(json1["instances"].keys())[0]]
    inst2 = json2["instances"][list(json2["instances"].keys())[0]]
    base_json["instances"][name1] = inst1
    base_json["instances"][name2] = inst2
    with open(name1+'_'+name2+'.json', 'w', encoding='utf-8') as f:
        json.dump(base_json, f, ensure_ascii=False, indent=4)

if __name__=='__main__':
    for name1 in trainset0:
        for name2 in trainset1:
            create_json(name1,name2)
    for name1 in valset0:
        for name2 in valset1:
            create_json(name1,name2)