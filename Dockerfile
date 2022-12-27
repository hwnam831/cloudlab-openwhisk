FROM openwhisk/python3aiaction:latest

RUN apt-get update
RUN apt-get install libjpeg-dev libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install numpy pandas scikit-learn minio
RUN pip install pillow psutil mxnet opencv-python
