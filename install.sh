wsk action create matmul matmul/matmul.py -m 512 --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create linpack linpack/linpack.py -m 512 --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create ml_training ml_training/__main__.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i -m 512
wsk action create cnn_serving cnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i -m 512
wsk action create image_rotate image_rotate/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create lr_serving lr_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i -m 512
wsk action create video_processing video_processing/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create rnn_serving rnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
