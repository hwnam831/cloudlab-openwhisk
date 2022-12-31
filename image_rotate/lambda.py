from PIL import Image
import os
import time
from minio import Minio

def getMinioClient(access, secret):
    return Minio(
        '10.10.1.1:9000',
        access_key = access,
        secret_key = secret,
        secure = False
    )

def main(params):
    startTime1 = time.time()
    minioClient = getMinioClient("minioadmin", "minioadmin")
    minioFile = minioClient.get_object('testbucket', 'image/image.jpg')
    image = Image.open(minioFile)
    endTime1 = time.time()
    startTime2 = time.time()
    img = image.transpose(Image.ROTATE_90)
    endTime2 = time.time()
    img.save('newImage.jpeg')
    with open('newImage.jpeg', 'rb') as testFile:
        statdata = os.stat('newImage.jpeg')
        startTime3 = time.time()
        minioClient.put_object(
            'testbucket',
            'image/newImage.jpg',
            testFile,
            statdata.st_size
        )
        endTime3 = time.time()

    print("Time 1 = ", endTime1 - startTime1)
    print("Time 2 = ", endTime2 - startTime2)
    print("Time 3 = ", endTime3 - startTime3)
    return {"Image":"rotated"}