FROM python:3.11-slim-bullseye

COPY run_model.py /

RUN pip install --upgrade pip
RUN pip install torch 
RUN pip install diffusers[torch] onnxruntime safetensors transformers xformers

RUN python run_model.py --downloadonly

ENTRYPOINT [ "bash" ]
