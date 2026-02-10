# 镜像构建：Packer

## 快速上手

Packer 是一个镜像构建器。曾经我们使用 [jenkins.clusters.zjusct.io](https://github.com/ZJUSCT/jenkins.clusters.zjusct.io)，基于 Shell 脚本使用 `systemd-nspawn` 或 `chroot` 执行构建。然而 Shell 脚本的可维护性、功能性可能比不上一个专用的镜像构建系统。在集群 K8S 建成后，我们切换到了 Packer。

建议新手阅读 Packer 官方文档 [HCL templates overview | Packer | HashiCorp Developer](https://developer.hashicorp.com/packer/docs/templates/hcl_templates)，同时借助 [canonical/packer-maas: Packer templates to create MAAS deployable images](https://github.com/canonical/packer-maas) 这一仓库学习如何使用 Packer 构建镜像。这是 Ubuntu MASS（裸金属集群管理平台）的镜像构建模板仓库，包含了各个发行版的 Packer 模板，并配备了简明的 README，十分值得参考。

## 使用

### HCL2 模板

!!! quote

    - [HCL templates overview | Packer | HashiCorp Developer](https://developer.hashicorp.com/packer/docs/templates/hcl_templates)

新版本的 Packer（v1.7.0 及以上）采用 HCL2 模板格式作为主要配置方式。只需要在项目目录中编写 `.pkr.hcl` 文件，即可描述镜像构建流程。

Builder 定义镜像构建的基础方式，常用的有：
● QEMU/KVM（本地构建qcow2）
● Openstack（用于构建交付到glance）
● docker（构建镜像容器）
在Openstack的场景下，我们通常使用qemu builder 构建 qcow2镜像。
示例：
source "qemu" "cloudimg" {
  format = "qcow2"
  disk_size = "6G"
}
Plugin（插件）
Packer 的 Builder 通常以插件形式提供，例如 qemu builder
如果模板中使用了如上的构建器，那么必须提供插件供初始化时安装：
packer {
  required_plugins {
    qemu = {
      source  = "github.com/hashicorp/qemu"
      version = ">= 1.1.0"
    }
  }
}
Provisioner（配置器）
Provisioner 用于在镜像构建过程中执行安装和配置动作，常见的类型为"shell""file""ansible"
provisioner "shell" {
  scripts = ["my-changes.sh"]
}
Provisioner 会在虚拟机内部执行脚本，进行必要的清理，安装工作，这同样是自动化配置自定义镜像OS的实现方式。
Post-processer（构建后处理）
Post-Processor 用于在镜像构建完成后处理输出文件，例如在提供glance所需的镜像时，我们需要对其进行扁平化处理：
post-processor "shell-local" {
    inline = [
      "set -euxo pipefail",
      "IN=output-cloudimg/packer-cloudimg",
      "qemu-img convert -p -f qcow2 -O qcow2 \"$IN\" \"ubuntu-${var.ubuntu_series}-${var.architecture}.qcow2\"",
      "qemu-img info \"ubuntu-${var.ubuntu_series}-${var.architecture}.qcow2\" | egrep -i 'file format|virtual size|disk size|backing file' || true"
    ]
    inline_shebang = "/bin/bash"
  }
Variables（变量）
变量在.pkr.hcl中用 var.* 的形式调用，可以在同名目录下通过.variables.pkr.hcl配置。在多文件版本里名为variables.pkr.hcl控制集体变量，而 *.variables.pkr.hcl单独添加该模板所需的变量。

### 命令

Packer 的使用通常分为两个核心步骤：

- 初始化：`pakcer init .`

    在首次执行构建前，需要先在模板目录下执行初始化。该命令会自动扫描当前目录中的 HCL 配置文件，并完成以下工作：

    - 解析模板中定义的 `packer.required_plugins` 块
    - 自动下载并安装所需插件（例如 qemu builder 插件）
    - 将插件缓存到本地目录（如 `.packer.d/plugins`）

- 构建镜像：`packer build`

    完成初始化后，即可执行镜像构建。Packer 会按照模板定义的流程自动执行：

    - 下载基础镜像（Ubuntu cloud image）
    - 启动 QEMU/KVM 虚拟机构建环境
    - 执行 provisioner 脚本进行系统定制
    - 清理镜像状态（cleanup）
    - 输出最终镜像文件（qcow2）

    可通过 `only` 参数指定当前目录下的构建目标

    ```shell
    packer build -only='cloudimg.*' .
    ```

