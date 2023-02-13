#!/bin/bash
cd /local/repository
bash setup-all.sh
wsk property set --apihost localhost:31001
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
bash install.sh
cd /mydata/workspace
git clone https://github.com/ddps-lab/serverless-faas-workbench
wget https://dl.minio.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo ./minio server /mydata/workspace/miniostorage/ &
#wget https://dl.min.io/server/minio/release/linux-amd64/minio_20230131022419.0.0_amd64.deb
#sudo dpkg -i minio_20230131022419.0.0_amd64.deb
#MINIO_ROOT_USER=minioadmin MINIO_ROOT_PASSWORD=minioadmin ./minio server /mydata/workspace/miniostorage --console-address ":9001" &
#sudo groupadd -r minio-user
#sudo useradd -M -r -g minio-user minio-user
#sudo chown minio-user:minio-user /mydata/workspace/miniostorage
#sudo cp /local/repository/miniodefault /etc/default/minio
#sudo systemctl start minio
wget https://dl.minio.io/client/mc/release/linux-amd64/mc
chmod +x mc
./mc alias set myminio/ http://10.10.1.1:9000 minioadmin minioadmin
./mc mb myminio/testbucket
./mc cp -r serverless-faas-workbench/dataset/* myminio/testbucket/
#git clone https://github.com/apache/openwhisk-runtime-python /mydata/workspace/openwhisk-runtime-python
#cd /mydata/workspace/openwhisk-runtime-python
#./gradlew core:python36AiAction:distDocker
#docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
#zip -r myaction.zip virtualenv __main__.py
#wsk action create myaction myaction.zip --kind python:3 -i
#wsk action create myaction myaction.py --docker openwhisk/python3aiaction
git clone https://github.com/PrincetonUniversity/faas-profiler /mydata/workspace/faas-profiler
cd /mydata/workspace/faas-profiler
git reset --hard b6f64dbfa9583e29c5679c1c9859b3818dc21638
bash configure.sh
cp /local/repository/*.json ./
wsk action create primes-python functions/microbenchmarks/primes/primes-python.py --docker hwnam831/mxcontainer:actionloop -i
wsk action create base64-python functions/microbenchmarks/base64/base64-python.py --docker hwnam831/mxcontainer:actionloop -i
cd functions/img-resize
sudo npm install node-zip jimp --save
zip -r action.zip ./*
wsk action create img-resize --kind nodejs:14 action.zip --web raw -i -m 4096
cd ../markdown-to-html/
wsk action create markdown2html markdown2html.py --docker immortalfaas/markdown-to-html --web raw -i
cd ../ocr-img/
wsk action create ocr-img handler.js --docker immortalfaas/nodejs-tesseract --web raw -i -m 4096
cd ../sentiment-analysis
wsk action create sentiment sentiment.py --docker immortalfaas/sentiment --web raw -i
cd ../..
./WorkloadInvoker -c warmup.json
#git clone https://github.com/spcl/serverless-benchmarks /mydata/workspace/sebs
#cd /mydata/workspace/sebs
#python3 /mydata/workspace/sebs/install.py --openwhisk
#. python-venv/bin/activate
#./sebs.py storage start minio --output-json config/minio.json
#jq --argfile file1 config/minio.json '.deployment.openwhisk.storage = $file1 ' config/example.json > config/ow.json
#echo "./sebs.py experiment invoke perf-cost --config config/ow.json --deployment openwhisk --verbose" > perf-cost.sh
#Check if minio works
#sudo systemctl status minio
wsk action invoke -i video_processing --result
