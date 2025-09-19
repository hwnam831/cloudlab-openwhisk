FROM python:3.11
RUN apt update
RUN pip install --upgrade pip
RUN pip install --yes torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN git clone https://github.com/pytorch/benchmark
WORKDIR /benchmark
RUN python install.py
RUN pip install .
ENTRYPOINT /bin/bash
