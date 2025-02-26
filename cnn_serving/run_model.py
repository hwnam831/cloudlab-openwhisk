import time
import random
import argparse
import os

from mxnet import gluon
import mxnet as mx
from PIL import Image



if __name__=='__main__':
    random.seed(17)
    os.environ['OMP_NUM_THREADS'] = "10"
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
    parser.add_argument(
        "--idle", type=float, default=0.3, help="idle percentage"
    )
    args = parser.parse_args()

    net = gluon.model_zoo.vision.resnet50_v1(pretrained=True, root = '/tmp/')
    net.hybridize(static_alloc=True, static_shape=True)
    lblPath = 'sysnet.txt'
    with open(lblPath, 'r') as f:
        labels = [l.rstrip() for l in f]

    #imgName = params["imgName"]
    imgName = 'animal-dog.jpg'
    source = mx.image.imread(imgName)
    
    #img = img.expand_dims(axis=0) # batchify
    curtime = time.time()
    endtime = curtime + args.duration
    while curtime < endtime and not args.downloadonly:
        #img = mx.image.imread(imgName)
        img = mx.image.imresize(source, 224, 224) # resize
        img = mx.image.color_normalize(img.astype(dtype='float32')/255,
                                    mean=mx.nd.array([0.485, 0.456, 0.406]),
                                    std=mx.nd.array([0.229, 0.224, 0.225])) # normalize
        img = img.transpose((2, 0, 1)) # channel first
        if args.workload == 'low':
            input = mx.nd.stack(img,img,axis=0)
        elif args.workload == 'med':
            input = mx.nd.stack(img,img,img,img,axis=0)
        elif args.workload == 'high':
            input = mx.nd.stack(img,img,img,img,img,img,img,img,img,img,img,img,img,img,img,img,axis=0)
        else:
            input = mx.nd.stack(img,img,img,img,axis=0)
        prob = net(input).softmax() # predict and normalize output
        idx = prob.topk(k=5)[0] # get top 5 result
        inference = ''
        for i in idx:
            i = int(i.asscalar())
            #print('With prob = %.5f, it contains %s' % (prob[0,i].asscalar(), labels[i]))
            inference = inference + 'With prob = %.5f, it contains %s' % (prob[0,i].asscalar(), labels[i]) + '. '
        elapsed = time.time() - curtime
        time.sleep(elapsed*args.idle)
        print(elapsed)
        curtime = time.time()
    # format image as (batch, RGB, width, height)