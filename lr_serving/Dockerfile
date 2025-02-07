FROM python:3.11-slim-bullseye

COPY run_model.py /

RUN apt update
RUN apt install -y git
RUN git clone https://github.com/ddps-lab/serverless-faas-workbench /serverless-faas-workbench
RUN pip install --upgrade pip
RUN pip install pandas joblib scikit_learn==0.22

ENTRYPOINT [ "bash" ]