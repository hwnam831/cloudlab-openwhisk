#!/bin/bash
cd /local/repository
bash setup-all.sh
python3 owPackageController.py &
git clone https://github.com/hwnam831/jRAPL-percore /mydata/workspace/jrapl
cd /mydata/workspace
wget https://download.pytorch.org/libtorch/nightly/cpu/libtorch-shared-with-deps-latest.zip
unzip libtorch-shared-with-deps-latest.zip
cd /mydata/workspace/jrapl
make
make install
