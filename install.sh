wsk action create matmul matmul/matmul.py -m 512 --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create linpack linpack/linpack.py -m 512 --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create ml_training ml_training/__main__.py -m 512 --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create cnn_serving cnn_serving/lambda.py -m 512 --docker hwnam831/actionloop-python-v3.6-ai:latest -i