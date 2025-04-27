# ZJUSCT 集群新手指南

!!! abstract

    本文档简单指引新成员熟悉集群环境。

!!! warning

    集群环境与个人电脑存在显著差异，请务必仔细阅读本指南。不当操作可能导致：

    - 性能显著下降
    - 数据丢失风险
    - 影响其他用户使用

## 集群架构概述

超算队自建有十余台服务器的集群，供竞赛、短学期课程和队员日常使用。

集群关键特性：

- **网络架构**：万兆以太网 + InfiniBand 高速网络
- **计算节点**：无盘系统设计

### 存储系统

| 挂载点 | 类型 | 容量 | 用途 |
|--------|------|------|------|
| `/` | OverlayFS+NFS | - | 系统根目录 |
| `/home` | NFS SSD | 8 TB(RAID10) | 用户家目录 |
| `/ocean` | NFS HDD | 21 TB(RAID60) | 冷数据 |
| `/river` | NFS SSD | 与 `/home` 共用 | 热数据 |
| `/local-sata`<br>`/local-nvme` | 本地 SSD | 按节点配置 | 本地磁盘，适用于低延迟任务 |

- **只有 `/` 不是持久存储**。
- **用途说明**：各挂载点根目录下有 `README` 文件，说明了各目录的用途，请自行查看。

    ```bash
    cat /ocean/README
    ```

    !!! tip

        - **家目录** 容量常年紧张，请及时清理。
        - 将模型、数据集等大文件存储在 `/ocean`（需要跨节点共享）或 `/local`（仅该节点使用）中。
        - **性能**：网络存储吞吐 ~1GB/s（万兆以太网），**小文件 IO 性能受限**。

- **快照保护**：所有存储池（`/home`、`/ocean` 和 `/river`）均有每日快照保护，保留 3 天。

!!! tip "关于 OverlayRoot"

    - 除了上述挂载点外，其他目录均为 `tmpfs`，会占用内存。如果使用过多可能引起 OOM。
    - 为了减小内存压力，目前 `/tmp`、`/var/tmp` 和 `/var/lib/docker` 均被挂载到 `/local` 下。

### 无盘系统

为了方便运维，集群采用无盘系统设计。细节见 [运维/系统运维/无盘系统](operation/system/diskless)。

- **引导方式**：PXE 网络引导
- **根文件系统**：OverlayFS + NFS Root
- **自动构建**：使用 [Jenkins](https://jenkins.zjusct.io/) 自动构建和更新根文件系统。
- **重要限制**：根目录 (`/`) 修改在重启后丢失，如通过 APT 安装的软件包等。

### 软件环境

- **包管理系统**：集群预装 Conda 和 Spack。

    ```bash
    # Conda 环境
    conda create -n myenv

    # Spack 包管理
    spack install hdf5
    ```

    - Conda 创建环境默认在个人家目录下，可以随意修改。
    - Spack 默认环境在 `/opt/spack` 下，无法修改。建议参照 [运维/软件运维/Spack](../operation/software/spack.md) 创建个人 Spack 环境。

- **预装目录**：`/opt`
- **配置管理**：[集群配置仓库](https://git.zju.edu.cn/zjusct/ops/jenkins.clusters.zjusct.io)

## 账户注册流程

向集群管理员申请，填写表单完成注册。随后，使用 SSH 登录集群。

```bash
ssh <username>@clusters.zju.edu.cn
```

!!! warning "所有超算队员拥有 root 权限，请保管好自己的 SSH 密钥和账户密码！"
