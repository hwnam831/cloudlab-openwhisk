FROM openwhisk/actionloop-python-v3.6-ai
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip install --upgrade pip
RUN pip install minio mxnet
RUN pip install pillow psutil
