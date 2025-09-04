sudo mkdir -p /mydata/docker
sudo mkdir -p /mydata/workspace
sudo modprobe msr
for FILE in /users/*; do
    CURRENT_USER=${FILE##*/}
    usermod -aG docker $CURRENT_USER
done

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
