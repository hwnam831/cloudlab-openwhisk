wsk action create matmul matmul/matmul.py --docker openwhisk/python3aiaction -i
wsk action create linpack linpack/linpack.py --docker openwhisk/python3aiaction -i
docker run --rm -v "$PWD/ml_training:/tmp" openwhisk/python3action bash -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install --no-input -r requirements.txt
