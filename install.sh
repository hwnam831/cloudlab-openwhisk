wsk action create -i matmul matmul/matmul.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i linpack linpack/linpack.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i ml_training ml_training/__main__.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i cnn_serving cnn_serving/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i image_rotate image_rotate/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i lr_serving lr_serving/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i video_processing video_processing/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i rnn_serving rnn_serving/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i sentiment sentiment-anlysis/sentiment.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i markdown2html markdown-to-html/markdown2html.py --docker hwnam831/mxcontainer:latest -m 2048

wsk action create -i matmul1 matmul/matmul.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i linpack1 linpack/linpack.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i ml_training1 ml_training/__main__.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i cnn_serving1 cnn_serving/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i image_rotate1 image_rotate/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i lr_serving1 lr_serving/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i video_processing1 video_processing/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i rnn_serving1 rnn_serving/lambda.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i sentiment1 sentiment-anlysis/sentiment.py --docker hwnam831/mxcontainer:latest -m 2048
wsk action create -i markdown2html1 markdown-to-html/markdown2html.py --docker hwnam831/mxcontainer:latest -m 2048