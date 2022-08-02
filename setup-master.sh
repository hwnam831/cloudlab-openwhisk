#!/bin/bash
git clone https://github.com/spcl/serverless-benchmarks /mydata/workspace/sebs
cd /mydata/workspace/sebs
python3 /mydata/workspace/sebs/install.py --openwhisk
. python-venv/bin/activate
./sebs.py storage start minio --output-json config/minio.json
jq --argfile file1 config/minio.json '.deployment.openwhisk.storage = $file1 ' config/example.json > config/ow.json
echo "./sebs.py experiment invoke perf-cost --config config/ow.json --deployment openwhisk --verbose" > perf-cost.sh
