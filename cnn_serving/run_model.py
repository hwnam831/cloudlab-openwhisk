import time
import random
import argparse
import os
import math
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
    parser.add_argument(
        "--tag", type=str, default='default', help="exp tag"
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
    begintime = time.time()
    curtime = begintime
    endtime = curtime + args.duration
    csvlines = []
    csvlines.append("Curtime,Elapsed")
    if args.workload == 'low':
        basearrivals = [0.31786687633244665, 0.8824637119454146, 1.0981153308313139, 1.2267388262786436, 1.2688335171244307, 
                        1.9371589204854913, 2.0269040923264123, 2.6701945276952346, 3.5579978738918783, 3.717259000128605, 
                        3.865525539921863, 4.137571622736609, 4.170420819085454, 4.219260405556031, 4.567611721038872, 
                        4.951368227680029, 5.01741793619966, 5.2255969337154795, 5.359001164508471, 5.709109465385991, 
                        5.729813944808159, 5.7660348771308625, 6.121232024152087, 6.739492939253424, 6.821919545776627, 
                        7.123959436512459, 7.386541614626432, 7.466147685784314, 7.620030066742997, 7.624045986727392, 
                        7.812593334689636, 8.083043543613925, 8.908919665696441, 9.000137005884026, 9.576461517424619, 
                        9.58511421217015, 9.6279491879051, 9.768063092040034, 9.845171989563081, 9.893774054647064]
        arrivals = []
        for i in range(0, 600, 10):
            newarrival = [x + i for x in basearrivals]
            arrivals += newarrival
    else: # high
        basearrivals = [0.7392597457198614, 1.3498220010031248, 2.0716777945249643, 3.5571865030643313, 3.729970221596453, 
                        7.569597144737793, 9.198512633020457, 10.828841475045232, 11.271415670369027, 11.81866007241221, 
                        12.398827892716383, 12.640796505054277, 13.58787180134101, 13.83720647484429, 14.031553983808033, 
                        14.35045477759978, 15.893234266696485, 16.85076000908753, 18.004283898418187, 18.500806375195143, 
                        21.10844262811711, 21.15512647843397, 21.94730608368767, 22.200280282066917, 22.351131006108094, 
                        22.575274741070984, 23.771096196213676, 24.052970465370205, 24.060222525062837, 25.935653114739818, 
                        26.407426360205115, 26.97463991686074, 27.29933758803466, 28.153166547553056, 28.510910759410393, 
                        28.70601946615806, 30.16491476244655, 30.260739306004727, 32.1499065067838, 32.741296340160794, 
                        32.773423787233895, 33.9291215868345, 34.32425472774691, 39.23638819976146, 43.421291740631, 
                        45.324564077019886, 46.530034773363276, 47.21813392260605, 47.94897427756322, 47.951944949772034, 
                        48.66211364776867, 50.30272180572789, 52.44700788118029, 53.20873127461086, 55.08838017294085, 
                        55.468799571253825, 55.54805572047232, 56.02687677451752, 56.15872341168355, 56.441701787770974, 
                        57.94736594659068]
        arrivals = []
        for i in range(0, 600, 60):
            newarrival = [x + i for x in basearrivals]
            arrivals += newarrival
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
            elapsed = time.time() - t - begintime
            logsum += math.log(elapsed)
            total += elapsed
            count += 1
            csvlines.append(f"{curtime},{elapsed}")
        gmean = math.exp(logsum/count)
        csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count}")
    with open(f"/mydata/workspace/jrapl/{args.tag}_cnn-serving_{args.workload}.csv", "w") as f:
        f.write("\n".join(csvlines))
    # format image as (batch, RGB, width, height)