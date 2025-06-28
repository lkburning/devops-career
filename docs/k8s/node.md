# 初始化Node 并加入 Master

本文将以ubuntu 为例，来说明如何配置一个k8s 的node 环境，并且使用 kubeadm 将其加入到master 节点中。

## 基于Ubuntu24.04 创建一个虚拟机

1. 打开你的本地浏览器登陆你的EXSI 的管理界面，如下所示
   ![img](../imgs/k8s/node/create_vm.png)
2. 创建一个虚拟机
   ![img](../imgs/k8s/node/create_vm_step1.png)
3. 指定你的虚拟机的名字以及系统的兼容性

   ![img](../imgs/k8s/node/create_vm_step2.png)
4. 配置你的虚拟机的需求（如，cpu，内存以及磁盘大小），并且指定从你的数据盘选中一个iso

   ![img](../imgs/k8s/node/create_vm_step3.png)
5. 等待虚拟机创建好，启动的虚拟机并按照知道配置你的操作系统。
6. 操作系统配置好以后，你就从EXSI 的管理界面上得到你的这台虚拟机的ip 地址，如下所示。这台机器的ip 是192.168.1.10
   ![img](../imgs/k8s/node/vm.png)

## 安装容器运行时

由于k8s 已经使用 containerd 作为默认的运行时，接下来我们将会安装 containerd 作为运行时。

在Ubunut 环境有两种方式安装Containerd, 一种是通过“From the official binaries“

### From the official binaries

office website: https://github.com/containerd/containerd/blob/main/docs/getting-started.md

#### Step 1 Installing containerd

Download the `containerd-<VERSION>-<OS>-<ARCH>.tar.gz` archive from [https://github.com/containerd/containerd/releases](https://github.com/containerd/containerd/releases) , verify its sha256sum, and extract it under `/usr/local`:

```shell
$ wget  https://github.com/containerd/containerd/releases/download/v2.1.1/containerd-2.1.1-linux-amd64.tar.gz
$ sudo tar Cxzvf /usr/local/ containerd-2.1.1-linux-amd64.tar.gz
bin/
bin/containerd-shim-runc-v2
bin/containerd
bin/containerd-stress
bin/ctr
```

##### systemd and proxy configure

If you intend to start containerd via systemd, you should also download the `containerd.service` unit file from [https://raw.githubusercontent.com/containerd/containerd/main/containerd.service](https://raw.githubusercontent.com/containerd/containerd/main/containerd.service) into `/lib/systemd/system/containerd.service`, and run the following commands:

```shell
$ sudo vim /lib/systemd/system/containerd.service
$ cat /lib/systemd/system/containerd.service
---------------------------------------------------
[Service]
#uncomment to enable the experimental sbservice (sandboxed) version of containerd/cri integration
#Environment="ENABLE_CRI_SANDBOXES=sandboxed"
Environment="HTTP_PROXY=http://192.168.1.125:7890/"
Environment="HTTPS_PROXY=http://192.168.1.125:7890/"
Environment="NO_PROXY=localhost,127.0.0.1,192.168.1.0/24,10.0.0.0/8"
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/bin/containerd
------------------------------------------------------

$ systemctl daemon-reload
$systemctl enable --now containerd
```

#### Step 2: Installing runc

Download the `runc.<ARCH>` binary from [https://github.com/opencontainers/runc/releases](https://github.com/opencontainers/runc/releases) , verify its sha256sum, and install it as `/usr/local/sbin/runc`.

```shell
$ wget https://github.com/opencontainers/runc/releases/download/v1.3.0/runc.amd64
$ sudo install -m 755 runc.amd64 /usr/local/sbin/runc
```

#### Step 3: Installing CNI plugins

Download the `cni-plugins-<OS>-<ARCH>-<VERSION>.tgz` archive from [https://github.com/containernetworking/plugins/releases](https://github.com/containernetworking/plugins/releases) , verify its sha256sum, and extract it under `/opt/cni/bin`:

```shell
$ wget https://github.com/containernetworking/plugins/releases/download/v1.7.1/cni-plugins-linux-amd64-v1.7.1.tgz
$ mkdir -p /opt/cni/bin
$ tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.7.1.tgz

```

#### step 4 start and generate the default config

```shell
$ containerd config default > containerd.config
$ sudo mkdir /etc/containerd/
$ sudo cp containerd.config /etc/containerd/config.toml
$ sudo systemctl start containerd
```

### 安装kubelet 并且安装 kubeadm ，并且禁止swap

1. 禁止swap 在 ubuntu

   ```
   sudo nano /etc/fstab
   # comment the line /swap.img       none    swap    sw      0       0
   sudo reboot

   ```
2. 安装kubectl 以及kubeadm

   ```
   sudo apt-get install -y apt-transport-https ca-certificates curl gpg
   curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
   echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
   sudo apt-get update
   sudo apt-get install -y kubelet kubeadm kubectl
   sudo apt-mark hold kubelet kubeadm kubectl


   ```

### 加入此Node 到 master 节点

1. 生成join 命令在master 节点

   ```
   kubeadm token create --print-join-command
   ```
2. 在node 节点使用sudo 执行命令，便可以成功加入节点

   ```
   sudo kubeadm join 192.168.1.11:6443 --token 08xg9j.j2mx8hwfh70qz5tj --discovery-token-ca-
   cert-hash sha256:a67b7bab9b024fb69c6aadb82b9f11e671ef5ec7881b06f23a54c9abf72bcbd0
   ```
3. 通过kubectl命令查看新加入的Node

   ```
   kubectl get nodes
   NAME              STATUS   ROLES           AGE     VERSION
   k8s-master        Ready    control-plane   15d     v1.32.5
   operation-node1   Ready    <none>          2m13s   v1.33.1
   ```
