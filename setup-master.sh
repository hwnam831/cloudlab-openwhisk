#!/bin/bash
wsk property set --apihost localhost:31001
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
sudo apt install ansible
git clone https://github.com/apache/openwhisk-runtime-python /mydata/workspace/openwhisk-runtime-python
cd /mydata/workspace/openwhisk-runtime-python
./gradlew core:python3Action:distDocker
git clone https://github.com/PrincetonUniversity/faas-profiler /mydata/workspace/faas-profiler
cd /mydata/workspace/faas-profiler
git reset --hard b6f64dbfa9583e29c5679c1c9859b3818dc21638
bash configure.sh
cp /local/repository/*.json ./
wsk action create primes-python functions/microbenchmarks/primes/primes-python.py -i
wsk action create base64-python functions/microbenchmarks/base64/base64-python.py -i
cd functions/img-resize
sudo npm install node-zip jimp --save
zip -r action.zip ./*
wsk action create img-resize --kind nodejs:14 action.zip --web raw -i
cd ../markdown-to-html/
wsk action create markdown2html markdown2html.py --docker immortalfaas/markdown-to-html --web raw -i
cd ../ocr-img/
wsk action create ocr-img handler.js --docker immortalfaas/nodejs-tesseract --web raw -i
cd ../sentiment-analysis
wsk action create sentiment sentiment.py --docker immortalfaas/sentiment --web raw -i
#git clone https://github.com/spcl/serverless-benchmarks /mydata/workspace/sebs
#cd /mydata/workspace/sebs
#python3 /mydata/workspace/sebs/install.py --openwhisk
#. python-venv/bin/activate
#./sebs.py storage start minio --output-json config/minio.json
#jq --argfile file1 config/minio.json '.deployment.openwhisk.storage = $file1 ' config/example.json > config/ow.json
#echo "./sebs.py experiment invoke perf-cost --config config/ow.json --deployment openwhisk --verbose" > perf-cost.sh
