---
tags:
  - 不完善
---

# ZJU Mirror 镜像站

!!! abstract

    本文档是 ZJU Mirror 最新的信息记录和运维手册。关于 Mirror 的历史和已废弃的运维信息，见 [ZJU Mirror 历史](mirror-history.md)。

## 简介

浙江大学开源软件镜像站 (<https://mirrors.zju.edu.cn>) 是由 [浙江大学信息中心](https://zuits.zju.edu.cn/) 支持、[浙江大学超算队](https://www.zjusct.io/) 运营的，致力于普及开源软件、方便校内外用户高效访问开源项目的各种资源的非营利计划。本镜像站提供了包括 Docker、PostgreSQL、Ubuntu 等项目的镜像，以服务教育和科学研究为目的，提倡自由、平等、协作、共享的精神。

### 丰富的镜像

浙大镜像站拥有 50+ 个镜像，包括 Anaconda、Ubuntu、Pypi、ArchLinux、Debian、Homebrew 等常用镜像，满足了校内师生日常使用的需求。我们也为大部分镜像提供了帮助文档，帮助用户快速完成配置。

### 标准化

#### 镜像获得官方认证

我们积极与上游联系，申请成为官方镜像。目前，已有 17 个镜像被认证为官方镜像，其中包括 Ubuntu、CentOS、ArchLinux、CTAN、ROS 等。成为官方镜像，证明我们服务的稳定性、实时性、正确性获得了官方的认可。

#### 接入[校园网联合镜像站](https://mirrors.cernet.edu.cn/)

校园网联合镜像站是由中国教育和科研计算机网网络中心支持的项目，它提供对校园网镜像站的索引和跳转服务。我们对接了标准化的接口，向外界暴露我们实时的资源使用情况和镜像同步状态信息。

### 透明

如果用户对镜像同步的实时性有质疑，可以访问镜像站网页，查看同步状态信息。如果用户希望知道更多的细节，可以访问 [浙大镜像站在校园网联合镜像站上的页面](https://mirrors.cernet.edu.cn/site/ZJU)，那里有更详细的同步状态信息。

### FAQ

!!! question "浙大镜像站相比于 [清华 TUNA 镜像站](https://mirrors.tuna.tsinghua.com/) 有什么优势？"

    - 浙大内网环境

    我们的服务器位于校园内网。根据我们的了解，不少实验室的网络存在公网访问速度慢、甚至无法访问公网的问题。使用我们浙大自己的镜像服务，即使没有公网访问的权限，依然可以正常使用镜像。

    - 高优支持校内师生

    我们会始终把支持校内用户放在最高优先级。即使是一些小众的镜像，只要浙大校内存在对这一镜像的稳定需求，我们一定会跟进、支持。就在最近，一位校内同学提出了添加 ius 镜像的请求。这一镜像的用户量非常小，使用场景也局限在旧的发行版中。但了解到这位同学的实验室只能访问校园内网，而且在做科研的过程中确实对这一镜像有需求，我们就满足了这一请求。此外，镜像服务在校内的可用性也是我们最高优保障的。使用其他学校的镜像站，可能就不会享受这方面的优势。

## 镜像站基础知识

!!! quote "其他镜像站"

    这里提供其他镜像站的文档指引。即使具体架构不同，镜像站运维仍有很多经验可以相互参考，我们提倡开源共享的精神。

    - [金枪鱼之夜：2023 年秋季学期迎新会 & TUNA 镜像站服务架构演进 | 清华大学 TUNA 协会](https://tuna.moe/event/2023/welcome-and-mirrors-infra/)
    - [开源镜像站 - LUG @ USTC](https://docs.ustclug.org/services/mirrors/)
    - [Home · sjtug/mirror-docker-unified Wiki](https://github.com/sjtug/mirror-docker-unified/wiki)

文档的接下来的内容面向镜像站爱好者和运维人员，本节总体介绍镜像站的构成和运维方式。

- **基础设施**：镜像站的硬件设施和网络环境，决定了镜像站上层采用的技术栈和运维方式。学校间的差异很大，从单机部署到云平台都有。
- **后端**：负责镜像站的核心任务——同步和存储，它主要是一个同步任务调度器。规模较大的镜像站几乎都会定制自己的后端，下面是国内镜像站后端简表：

    | 语言 | 后端实现 |
    | --- | --- |
    | Go | [tuna/tunasync](https://github.com/tuna/tunasync)、[sjutg/lug](https://github.com/sjtug/lug)、[ustclug/Yuki](https://github.com/ustclug/Yuki) |
    | Python | [PKUOSC](https://github.com/PKUOSC/SyncController) |
    | C# | [ZJUSCT/MirrorManager](https://github.com/ZJUSCT/MirrorManager) |

- **前端**：负责镜像站的访问和用户交互。它主要是 Web 服务，提供了镜像列表、同步状态、帮助文档等功能。

## 基础设施

!!! quote

    - [Support - 02-PCIe network adapter specifications- H3C](https://www.h3c.com/en/Support/Resource_Center/EN/Severs/Catalog/Optional_Parts/Network_Adapter/Technical_Documents/Product_Literature/Card_Datasheets/Network_Adapter_Datasheet/202206/1616867_294551_0.htm)：新华三网卡数据表。
    - [Support - 08-Configuring an H460, P460, P240 or P4408 storage controller- H3C](https://www.h3c.com/en/Support/Resource_Center/EN/Home/Severs/00-Public/Software_Configure/User_Manual/H3C_Servers_Storage_Controller_UG/202207/1655190_294551_0.htm)：RAID 卡配置手册。

浙江大学镜像站所有的硬件资源都是由浙大信息中心赞助的。镜像站属于信息中心 [研在浙大·科研软件平台](https://soft.zju.edu.cn/) 的一个子项目。

2025 年 4 月 17 日，我们从信息技术中心收到了新一代镜像站的硬件设施。新一代镜像站由 3 台存储服务器、2 台业务服务器构成，通过万兆交换机互联。

![infra](mirror.assets/infra.drawio)

### 存储服务器 [H3C X10536 G3](https://www.h3c.com/cn/Service/Document_Software/Document_Center/Storage/Catalog/Massive_Scale_Out/H3C_UniStor_X10000_G3/)

| 参数 | 值 |
| --- | --- |
| CPU | 2 x Intel Xeon Silver 4110 |
| 内存 | 8 x 32GB DDR4 2666MHz RDIMM |

- 存储规格：每台配备 2 张 4GB 缓存 RAID 卡。其上连接的存储设备有：

| 数量 | 容量 | 类型 | 具体型号 |
| --- | --- | --- | --- |
| 2 | 600G | 12 Gbps SAS HDD 系统盘 | SEAGATE ST600MM0009 |
| 6 | 480GB | 12 Gbps SATA SSD 数据盘 | Micron 5200 MTFD |
| 30 | 8TB | 12 Gbps SATA HDD 数据盘 | SEAGATE ST8000NM0055-1RM |

- 网络规格：每台配备 2 张双口 10G 以太网卡和 1 张双 1G 以太网卡。

| 插槽 | 网卡型号 | 规格 | 控制器 |
| --- | --- | --- | --- |
| PCIe | CNA-10GE-2P-560F-B2-1 | 2 x 10GE SFP | Intel JL82599 |
| PCIe | NIC-GE-2P-360T-B2-1-X | 2 x 1GE RJ45 | Intel NHI350AM |
| FLOM | NIC-10GE-2P-560F-LOM | 2 x 10GE SFP | Intel JL82599 |

### 业务服务器 [H3C R4900 G3](https://www.h3c.com/cn/Service/Document_Software/Document_Center/Server/Catalog/Rack_server/H3C_UniServer_R4900_G3/)

| 参数 | 值 |
| --- | --- |
| CPU | 2 x Intel Xeon Gold 6130 |
| 内存 | 6 x 16GB DDR4 2666MHz RDIMM |

- 存储规格：每台配备 1 张 4GB 缓存 RAID 卡，已配置为 RAID1。其上连接的存储设备有：

| 数量 | 容量 | 类型 | 具体型号 |
| --- | --- | --- | --- |
| 2 | 600G | 12 Gbps SAS HDD 系统盘 | SEAGATE ST600MM0009 |

- 网络规格：每台配备 1 张双口 10G 以太网卡。

| 插槽 | 网卡型号 | 规格 | 控制器 |
| --- | --- | --- | --- |
| PCIe | NIC-BCM957302-F-B-10Gb-2P | 2 x 10GE SFP | Broadcom BCM57302 |

### 交换机 [H3C S6520X-24ST-SI](https://www.h3c.com/cn/Products_And_Solution/InterConnect/Products/Switches/Products/Park_Switches/Aggregation_Switch/S6500/S6520X-SI/)

| 参数 | 值 |
| --- | --- |
| 前面板业务端口描述 | 24 个 1/2.5/10GE SFP Plus 端口（2 个 Combo 1G/2.5G/5G/10G Base-T 自适应以太网端口） |
| 交换容量 | 2.56Tbps/25.6Tbps |
| 包转发率 | 360Mpps |
| 链路聚合 | 支持 10GE 端口聚合 |

## 后端


## 前端



