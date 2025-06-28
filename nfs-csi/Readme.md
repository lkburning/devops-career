# Install Nfs csi driver

Install the csi driver according https://github.com/kubernetes-csi/csi-driver-nfs/tree/master/charts

```shell
$ helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
$ helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs --namespace kube-system --version 4.11.0 -f helm/values.yaml
```
