wsk action create matmul matmul/matmul.py --docker openwhisk/python3aiaction -i
wsk action create linpack linpack/linpack.py --docker openwhisk/python3aiaction -i
docker run --rm -v "$PWD/ml_training:/tmp" openwhisk/python3aiaction bash -c "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install --no-input -r requirements.txt"
cd ml_training
zip -r ml_training.zip virtualenv __main__.py
wsk action create ml_training ml_training.zip --kind python:3 --docker openwhisk/python3aiaction -i
cd ..

