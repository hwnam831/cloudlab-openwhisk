#!/bin/bash
cd /local/repository
bash setup-all.sh
python3 owPackageController.py &
cd /mydata/workspace
wget https://download.pytorch.org/libtorch/nightly/cpu/libtorch-shared-with-deps-latest.zip
unzip libtorch-shared-with-deps-latest.zip
