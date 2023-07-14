#!/bin/bash
cd /local/repository
wsk property set --apihost localhost:31001
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
bash install.sh
cd /mydata/workspace

cd /mydata/workspace/faas-profiler
wsk action create primes-python functions/microbenchmarks/primes/primes-python.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create base64-python functions/microbenchmarks/base64/base64-python.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create primes-python_socket1 functions/microbenchmarks/primes/primes-python.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
wsk action create base64-python_socket1 functions/microbenchmarks/base64/base64-python.py --docker hwnam831/actionloop-python-v3.6-ai:latest -i
cd functions/img-resize
sudo npm install node-zip jimp --save
zip -r action.zip ./*
wsk action create img-resize --kind nodejs:14 action.zip --web raw -i -m 512
wsk action create img-resize_socket1 --kind nodejs:14 action.zip --web raw -i -m 512
cd ../markdown-to-html/
wsk action create markdown2html markdown2html.py --docker immortalfaas/markdown-to-html --web raw -i
wsk action create markdown2html_socket1 markdown2html.py --docker immortalfaas/markdown-to-html --web raw -i
cd ../ocr-img/
wsk action create ocr-img handler.js --docker immortalfaas/nodejs-tesseract --web raw -i -m 512
wsk action create ocr-img_socket1 handler.js --docker immortalfaas/nodejs-tesseract --web raw -i -m 512
cd ../sentiment-analysis
wsk action create sentiment sentiment.py --docker immortalfaas/sentiment --web raw -i
wsk action create sentiment_socket1 sentiment.py --docker immortalfaas/sentiment --web raw -i
cd ../..

wsk action invoke -i video_processing --result
