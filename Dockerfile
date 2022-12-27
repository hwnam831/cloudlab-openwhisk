FROM openwhisk/python3action:latest

RUN apk add --update py-pip
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx libjpeg-dev
RUN pip install numpy pandas scikit-learn minio
RUN pip install pillow psutil mxnet opencv-python
RUN pip install torch
