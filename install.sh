wsk action create matmul matmul/matmul.py --docker hwnam831/python3aiaction:mlhrc -i
wsk action create linpack linpack/linpack.py --docker hwnam831/python3aiaction:mlhrc -i
wsk action create ml_training ml_training/__main__.py -m 2048 --docker hwnam831/python3aiaction:mlhrc -i

