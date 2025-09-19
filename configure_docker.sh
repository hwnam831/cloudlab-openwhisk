sudo mkdir -p /mydata/docker
sudo mkdir -p /mydata/workspace
sudo chmod 777 /mydata/workspace
sudo modprobe msr
for FILE in /users/*; do
    CURRENT_USER=${FILE##*/}
    sudo usermod -aG docker $CURRENT_USER
done
newgrp docker
echo -e '{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "100m"
    },
    "storage-driver": "overlay2",
    "data-root": "/mydata/docker"
}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker || (echo "ERROR: Docker installation failed, exiting." && exit -1)
sudo docker run hello-world | grep "Hello from Docker!" || (echo "ERROR: Docker installation failed, exiting." && exit -1)
sudo docker pull hwnam831/torchbench

git clone https://github.com/hwnam831/jRAPL-percore /mydata/workspace/jrapl
cd /mydata/workspace/jrapl
make
make install
