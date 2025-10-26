import time
import random
import argparse
import os
import math
from mxnet import gluon
import mxnet as mx
from PIL import Image
import numpy as np

def PoissonGen(rate, interval, seed=1):
    n = int(rate*interval)
    random.seed(seed)
    arr = [-np.log(random.random())/rate for _ in range(2*n)]
    acc = 0
    times = []
    for t in arr:
        acc += t
        if acc > interval:
            break
        times.append(acc)
    return times

if __name__=='__main__':
    random.seed(17)
    os.environ['OMP_NUM_THREADS'] = "28"
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
    parser.add_argument(
        "--tag", type=str, default='default', help="exp tag"
    )
    parser.add_argument(
        "--continuous",
        action="store_true"
    )
    parser.add_argument(
        "--config", type=int, default=1,choices=[1,2,3,4], help="Arrival trace choice"
    )
    args = parser.parse_args()

    net = gluon.model_zoo.vision.resnet152_v2(pretrained=True, root = '/tmp/')
    net.hybridize(static_alloc=True, static_shape=True)
    lblPath = 'sysnet.txt'
    with open(lblPath, 'r') as f:
        labels = [l.rstrip() for l in f]

    #imgName = params["imgName"]
    imgName = 'animal-dog.jpg'
    source = mx.image.imread(imgName)
    
    #img = img.expand_dims(axis=0) # batchify
    begintime = time.time()
    curtime = begintime
    endtime = curtime + args.duration
    csvlines = []
    csvlines.append("Curtime,Elapsed,Batchsize")
    if args.workload == 'low':
        arrivals = PoissonGen(5, args.duration, args.config)
        bsize = 8
    elif args.workload == 'med':
        arrivals = PoissonGen(1.5, args.duration, args.config)
        bsize = 8
    elif args.workload == 'high':
        arrivals = PoissonGen(2, args.duration, args.config)
        bsize = 32
    else: # high
        arrivals = PoissonGen(1, args.duration, args.config)
        bsize = 4
        
    '''
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
        csvlines.append(f"{curtime-begintime},{elapsed}")
        time.sleep(elapsed*args.idle)
        curtime = time.time()
    '''
    if (not args.downloadonly):
        logsum = 0
        total = 0
        count = 0
        if args.continuous:
            while curtime < endtime:
                img = mx.image.imresize(source, 224, 224) # resize
                img = mx.image.color_normalize(img.astype(dtype='float32')/255,
                                            mean=mx.nd.array([0.485, 0.456, 0.406]),
                                            std=mx.nd.array([0.229, 0.224, 0.225])) # normalize
                img = img.transpose((2, 0, 1)) # channel first
                if args.workload == 'low':
                    input = mx.nd.stack(img,img,img,img,img,img,img,img,axis=0)
                elif args.workload == 'med':
                    input = mx.nd.stack(img,img,img,img,img,img,img,img,axis=0)
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
                logsum += math.log(elapsed)
                total += elapsed
                count += 1
                csvlines.append(f"{curtime-begintime},{elapsed}")
                curtime = time.time()
        else:
            for t in arrivals:
                curtime = time.time() - begintime
                if t > args.duration:
                    break
                if curtime < t:
                    time.sleep(t-curtime)
                img = mx.image.imresize(source, 224, 224) # resize
                img = mx.image.color_normalize(img.astype(dtype='float32')/255,
                                            mean=mx.nd.array([0.485, 0.456, 0.406]),
                                            std=mx.nd.array([0.229, 0.224, 0.225])) # normalize
                img = img.transpose((2, 0, 1)) # channel first
                if args.workload == 'low':
                    input = mx.nd.stack(img,img,img,img,axis=0)
                elif args.workload == 'med':
                    input = mx.nd.stack(img,img,img,img,img,img,img,img,axis=0)
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
                elapsed = time.time() - t - begintime
                logsum += math.log(elapsed)
                total += elapsed
                count += 1
                csvlines.append(f"{curtime},{elapsed},{bsize}")
        gmean = math.exp(logsum/count)
        #csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count},{bsize}")
    with open(f"/mydata/workspace/jrapl/{args.tag}_cnn-serving_{args.workload}.csv", "w") as f:
        f.write("\n".join(csvlines))
    # format image as (batch, RGB, width, height)