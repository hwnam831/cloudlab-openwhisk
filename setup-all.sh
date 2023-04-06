#!/bin/bash
sudo mkdir /mydata/workspace
sudo chown hwnam831 /mydata/workspace

sudo apt install --yes libpfm4-dev cpufrequtils msr-tools cmake
sudo modprobe msr
#sudo wrmsr --all 0x1a0 0x4000850089
git config --global user.email "hwnam831@gmail.com"
git config --global user.name "Hyoungwook Nam"
#docker pull hwnam831/mxcontainer:latest
#docker pull hwnam831/invoker:v2
#docker pull hwnam831/controller:v2
