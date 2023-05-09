import json
import random

trainset = ['ml_training', 'cnn_serving', 'base64', 'matmul', 'rnn_serving', 'image_rotate']
valset = ['linpack', 'lr_serving', 'primes', 'video_processing']

def create_json(name1, name2):
    dirname = 'mxcontainerconfigs/'
    base_json = {"test_duration_in_seconds": 90,
    "blocking_cli": False}
    base_json["random_seed"] = random.randint(0,100)
    base_json["test_name"] = name1 + "_" + name2
    base_json["instances"] = {}
    json1 = json.load(open(name1 + '.json','r'))
    json2 = json.load(open(name2 + '.json','r'))
    inst1 = json1["instances"][list(json1["instances"].keys())[0]]
    inst2 = json2["instances"][list(json2["instances"].keys())[0]]
    inst2["application"] = inst2["application"] + '1'
    base_json["instances"][name1] = inst1
    base_json["instances"][name2] = inst2
    
    with open(dirname+name1+'_'+name2+'.json', 'w', encoding='utf-8') as f:
        json.dump(base_json, f, ensure_ascii=False, indent=4)

if __name__=='__main__':
    for i in range(len(trainset)):
        for j in range(i+1,len(trainset)):
            name1 = trainset[i]
            name2 = trainset[j]
            create_json(name1,name2)
            create_json(name2,name1)
            
    for i in range(len(valset)):
        for j in range(i+1,len(valset)):
            name1 = valset[i]
            name2 = valset[j]
            create_json(name1,name2)
            create_json(name2,name1)