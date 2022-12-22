import time
import psutil
import os
pid = os.getpid()
python_process = psutil.Process(pid)
memoryUse_old = 0
t1 = time.time()

from mxnet import gluon
import mxnet as mx
from minio import Minio
from PIL import Image

t2 = time.time()
memoryUse = python_process.memory_info()[0]/2.**30
print('memory use 1:', memoryUse-memoryUse_old)

def getMinioClient(access, secret):
    return Minio(
        '172.22.224.2:9000',
        access_key = access,
        secret_key = secret,
        secure = False
    )

minioClient = getMinioClient("minioadmin", "minioadmin")
net = gluon.model_zoo.vision.resnet50_v1(pretrained=True, root = '/tmp/')
net.hybridize(static_alloc=True, static_shape=True)
lblPath = gluon.utils.download('http://data.mxnet.io/models/imagenet/synset.txt',path='/tmp/')
with open(lblPath, 'r') as f:
    labels = [l.rstrip() for l in f]
t3 = time.time()
memoryUse_old = memoryUse
memoryUse = python_process.memory_info()[0]/2.**30
print('memory use 2:', memoryUse-memoryUse_old)

def main(params):
    imgName = params["imgName"]
    minioFile = minioClient.get_object('testbucket', imgName)
    image = Image.open(minioFile)
    image.save('tempImage.jpeg')

    # format image as (batch, RGB, width, height)
    img = mx.image.imread("tempImage.jpeg")
    img = mx.image.imresize(img, 224, 224) # resize
    img = mx.image.color_normalize(img.astype(dtype='float32')/255,
                                mean=mx.nd.array([0.485, 0.456, 0.406]),
                                std=mx.nd.array([0.229, 0.224, 0.225])) # normalize
    img = img.transpose((2, 0, 1)) # channel first
    img = img.expand_dims(axis=0) # batchify

    prob = net(img).softmax() # predict and normalize output
    idx = prob.topk(k=5)[0] # get top 5 result
    inference = ''
    for i in idx:
        i = int(i.asscalar())
        print('With prob = %.5f, it contains %s' % (prob[0,i].asscalar(), labels[i]))
        inference = inference + 'With prob = %.5f, it contains %s' % (prob[0,i].asscalar(), labels[i]) + '. '

    t4 = time.time()
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 3:', memoryUse-memoryUse_old)

    return inference