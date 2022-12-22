wsk action create matmul matmul/matmul.py --docker openwhisk/python3aiaction -i
wsk action create linpack linpack/linpack.py --docker openwhisk/python3aiaction -i