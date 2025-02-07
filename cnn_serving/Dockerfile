FROM hwnam831/actionloop-python-v3.6-ai:latest

RUN pip install --upgrade pip
RUN pip install mxnet-mkl 

COPY run_model.py /
COPY animal-dog.jpg /
COPY sysnet.txt /

RUN python run_model.py --downloadonly
ENV OMP_NUM_THREADS=10

ENTRYPOINT [ "bash" ]