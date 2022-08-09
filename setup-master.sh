#!/bin/bash
git clone https://github.com/PrincetonUniversity/faas-profiler /mydata/workspace/faas-profiler
cd /mydata/workspace/faas-profiler
bash configure.sh
cd functions/img-resize
sudo npm install node-zip jimp --save
zip -r action.zip ./*
wsk action create img-resize --kind nodejs:12 action.zip --web raw -i
cd ../markdown-to-html/
wsk action create markdown2html markdown2html.py --docker immortalfaas/markdown-to-html --web raw -i
cd ../ocr-img/
wsk action create ocr-img handler.js --docker immortalfaas/nodejs-tesseract --web raw -i
cd ../sentiment-analysis
#git clone https://github.com/spcl/serverless-benchmarks /mydata/workspace/sebs
#cd /mydata/workspace/sebs
#python3 /mydata/workspace/sebs/install.py --openwhisk
#. python-venv/bin/activate
#./sebs.py storage start minio --output-json config/minio.json
#jq --argfile file1 config/minio.json '.deployment.openwhisk.storage = $file1 ' config/example.json > config/ow.json
#echo "./sebs.py experiment invoke perf-cost --config config/ow.json --deployment openwhisk --verbose" > perf-cost.sh
