FROM python:3.11-slim-bullseye

COPY run_model.py /

RUN pip install --upgrade pip
RUN pip install torch 
RUN pip install huggingface-hub onnxruntime safetensors transformers xformers accelerate

RUN huggingface-cli login --token $(cat huggingfacetoken)

RUN python run_model.py --downloadonly

ENTRYPOINT [ "bash" ]