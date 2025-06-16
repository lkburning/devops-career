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

在Ubunut 环境有两种方式安装Containerd, 一种是通过“From the official binaries“，第二种便是 ”From `apt-get` or `dnf`”，出于方便考虑，我们使用apt-get 进行安装

### From apt-get install Containerd

office website: https://docs.docker.com/engine/install/ubuntu/

#### [Uninstall old versions](https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions)

```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

### [Install using the `apt` repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

1. Set up Docker's `apt` repository.

   ```
   # Add Docker's official GPG key:
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   ```
2. Install the Docker packages.

   ```
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
3. [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

   ```
   sudo groupadd docker
   sudo usermod -aG docker $USER
   newgrp docker
   ```
