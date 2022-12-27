FROM tensorflow/tensorflow:latest
RUN apt update
RUN apt -y install libjpeg-dev libgl1-mesa-glx libglib2.0-0
RUN pip install --upgrade pip
RUN pip install numpy pandas scikit-learn minio
RUN pip install pillow psutil mxnet opencv-python
