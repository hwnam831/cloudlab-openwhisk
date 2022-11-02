#!/bin/bash
sudo mkdir /mydata/workspace
sudo chown hwnam831 /mydata/workspace
git clone https://github.com/hwnam831/jRAPL-percore /mydata/workspace/jrapl
cd /mydata/workspace/jrapl
make
make install
sudo apt install libpfm4-dev cpufrequtils msr-tools
sudo modprobe msr
#sudo wrmsr --all 0x1a0 0x4000850089
git config --global user.email "hwnam831@gmail.com"
git config --global user.name "Hyoungwook Nam"
