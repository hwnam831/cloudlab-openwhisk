import time
import psutil
import os
pid = os.getpid()
python_process = psutil.Process(pid)
memoryUse_old = 0
t1 = time.time()
import cv2

memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
print('memory use 1:', memoryUse-memoryUse_old)
t2 = time.time()

tmp = "/tmp/"

vid1_name = '/home/jovans2/apps/video_processing/vid1.mp4'
vid2_name = '/home/jovans2/apps/video_processing/vid2.mp4'

result_file_path = tmp + vid2_name

video = cv2.VideoCapture(vid2_name)

width = int(video.get(3))
height = int(video.get(4))
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (width, height))

t3 = time.time()

def video_processing():
    timeO = 0
    while video.isOpened():
        ret, frame = video.read()
        start = time.time()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            #gray_frame = cv2.imread(tmp_file_path)
            #out.write(gray_frame)
            break
        else:
            break
        end = time.time()
        timeO += end - start
    video.release()
    out.release()
    return

def main(params):

    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 2:', memoryUse-memoryUse_old)

    video_processing()

    t4 = time.time()
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 3:', memoryUse-memoryUse_old)