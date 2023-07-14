wsk action create -i matmul matmul/matmul.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i linpack linpack/linpack.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i ml_training ml_training/__main__.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i cnn_serving cnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i image_rotate image_rotate/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 1024
wsk action create -i lr_serving lr_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i video_processing video_processing/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i rnn_serving rnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512

wsk action create -i matmul_socket1 matmul/matmul.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i linpack_socket1 linpack/linpack.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i ml_training_socket1 ml_training/__main__.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i cnn_serving_socket1 cnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i image_rotate_socket1 image_rotate/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 1024
wsk action create -i lr_serving_socket1 lr_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i video_processing_socket1 video_processing/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
wsk action create -i rnn_serving_socket1 rnn_serving/lambda.py --docker hwnam831/actionloop-python-v3.6-ai:latest -m 512
