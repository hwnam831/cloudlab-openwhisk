#!/bin/bash
sudo mkdir /mydata/workspace
sudo chown hwnam831 /mydata/workspace
git clone https://github.com/hwnam831/jRAPL-percore /mydata/workspace/jrapl
sudo modprobe msr
sudo apt install msr-utils
sudo wrmsr --all 0x1a0 0x4000850089
