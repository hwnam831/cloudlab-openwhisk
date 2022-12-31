import time
import psutil
import os
import cv2
from minio import Minio

def video_processing(object_key, video_path):
    file_name = object_key.split(".")[0]
    tmp = '/tmp'
    result_file_path = tmp+file_name+'-output.avi'

    video = cv2.VideoCapture(video_path)
    
    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time.time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    latency = time.time() - start

    video.release()
    out.release()
    return latency, result_file_path

def getMinioClient(access, secret):
    return Minio(
        '10.10.1.1:9000',
        access_key = access,
        secret_key = secret,
        secure = False
    )

def main(params):
    pid = os.getpid()
    python_process = psutil.Process(pid)
    memoryUse_old = 0
    t1 = time.time()
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think

    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 2:', memoryUse-memoryUse_old)
    tmp = "/tmp/"

    vid_name = 'SampleVideo_1280x720_10mb.mp4'
    minioClient = getMinioClient("minioadmin", "minioadmin")

    minioClient.fget_object('testbucket', 'video/'+vid_name, tmp+vid_name)
    print('memory use 1:', memoryUse-memoryUse_old)
    t2 = time.time()



    latency, result_file = video_processing(vid_name, tmp+vid_name)

    t3 = time.time()


    t4 = time.time()
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 3:', memoryUse-memoryUse_old)
    return {'latency':latency}