#!/bin/bash
#usage: bash init_containers.sh [containername] [socket]
NCPUS=$(nproc)
SOCKETCPUS=$((NCPUS/2))
OFFSET=$(($2 * $SOCKETCPUS + 1))
CPUSET="$OFFSET-$(($OFFSET + $SOCKETCPUS - 2))"
sudo docker run -d -it --cpuset-cpus=$CPUSET --name="$1_$2" hwnam831/$1