cd /home/cloudlab-openwhisk/openwhisk-deploy-kube
sudo helm uninstall owdev -n openwhisk
kubectl delete namespace openwhisk; kubectl create namespace openwhisk
sudo helm install owdev ./helm/openwhisk -n openwhisk -f mycluster.yaml