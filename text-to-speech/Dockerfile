FROM python:3.11-slim-bullseye

COPY run_model.py /
#COPY huggingfacetoken /

RUN apt update
RUN apt install -y espeak-ng

RUN pip install --upgrade pip
RUN pip install torch scipy
RUN pip install huggingface-hub onnxruntime safetensors transformers xformers accelerate
RUN pip install phonemizer

#RUN huggingface-cli login --token $(cat huggingfacetoken)

RUN python run_model.py --downloadonly

ENTRYPOINT [ "bash" ]
