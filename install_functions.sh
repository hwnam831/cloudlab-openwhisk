#!/bin/bash
cd /local/repository
wsk property set --apihost localhost:31001
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
bash install.sh
cd /mydata/workspace

cd /mydata/workspace/faas-profiler
git reset --hard b6f64dbfa9583e29c5679c1c9859b3818dc21638
bash configure.sh
cp /local/repository/*.json ./
wsk action create primes-python functions/microbenchmarks/primes/primes-python.py --docker hwnam831/mxcontainer:v2 -i
wsk action create base64-python functions/microbenchmarks/base64/base64-python.py --docker hwnam831/mxcontainer:v2 -i
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

wsk action invoke -i video_processing --result
