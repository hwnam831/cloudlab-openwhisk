wsk action create -i matmul matmul/matmul.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i linpack linpack/linpack.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i ml_training ml_training/__main__.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i cnn_serving cnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i image_rotate image_rotate/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i lr_serving lr_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i video_processing video_processing/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i rnn_serving rnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
