FROM openwhisk/action-python-v3.7:1.17.0

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx libjpeg-dev libglib2.0-0 libsm6 libxrender1 libxext6 libgomp1 libquadmath0
RUN pip install --upgrade pip
RUN pip install pandas minio
RUN pip3 install "scikit_learn==0.22.2.post1"
RUN pip3 install mxnet-mkl==1.6.0 
RUN pip install pillow psutil opencv-python
RUN pip install torch
RUN pip install sockets pickle-mixin requests js2py JPype1 redis
RUN pip install textblob
RUN python -m textblob.download_corpora
RUN pip install markdown
