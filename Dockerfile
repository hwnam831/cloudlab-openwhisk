FROM openwhisk/python3aiaction:latest
RUN apt-get update
RUN apt-get -y install libjpeg-dev libgl1-mesa-glx libglib2.0-0
RUN pip install --upgrade pip
RUN pip install opencv-python
RUN pip install pillow psutil minio
