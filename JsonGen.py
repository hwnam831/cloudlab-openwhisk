import json
import random

functions = ['base64', 'image_rotate', 'linpack', 'lr_serving', 'matmul', 'ml_training', 'ocr-img', 'primes', 'rnn_serving', 'video_processing']
dirname = 'mlcontrolconfigs/'

def create_json(name1, name2):
    base_json = {"test_duration_in_seconds": 10,
    "blocking_cli": False}
    base_json["random_seed"] = random.randint(0,100)
    base_json["test_name"] = name1 + "_" + name2
    base_json["instances"] = {}
    json1 = json.load(open(name1 + '.json','r'))
    json2 = json.load(open(name2 + '.json','r'))
    inst1 = json1["instances"][list(json1["instances"].keys())[0]]
    inst2 = json2["instances"][list(json2["instances"].keys())[0]]
    inst2["application"] = inst2["application"] + "_socket1"
    base_json["instances"][name1] = inst1
    base_json["instances"][name2] = inst2
    with open(dirname + name1+'_'+name2+'.json', 'w', encoding='utf-8') as f:
        json.dump(base_json, f, ensure_ascii=False, indent=4)

if __name__=='__main__':
    for i in range(len(functions)):
        for j in range(len(functions)):
            if i == j:
                continue
            create_json(functions[i],functions[j])
