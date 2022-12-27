wsk action create matmul matmul/matmul.py --docker openwhisk/python3aiaction -i
wsk action create linpack linpack/linpack.py --docker openwhisk/python3aiaction -i
wsk action create ml_training ml_training/__main__.py -m 2048 --docker hwnam831/python3mlhrc -i

