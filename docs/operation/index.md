---
tags:
  - 完善
---

# 运维文档

## 运维文档导航

运维文档结构按照运维工作的不同方面进行划分。参与运维工作的同学可以选择自己感兴趣的部分进行学习，也可以根据任务需要进行查阅。**目前运维工作的重心在软件运维。**

<div class="grid cards" markdown>

!!! warning "[硬件运维](hardware/index.md)"

    - 内容：
        - 硬件设备的相关知识和经验，进入机房或进行硬件操作时请参考该部分文档。
        - 集群中硬件设备的文档收集。
    - 相关任务：每月会有一两次更换设备的需求，线下比赛时搭建集群。

!!! abstract "[网络运维](network/index.md)"

    - 内容：
        - 以太网：企业级交换机和路由器的配置方法，VLAN、DHCP Snooping 等常见网络技术。
        - 高性能网络：InfiniBand 网络原理，RDMA 等技术。
    - 相关任务：
        - 监控网络情况，排查网络故障。
        - 线下比赛时根据需求组建网络。
        - 对高性能网络进行排障和调优。

!!! question "[系统运维](system/index.md)"

    - 内容：
        - 目前集群使用基于 PXE 和 NFS Root 的无盘系统，这里介绍这套系统的部署和维护方式。
        - 完整的集群包含一整套服务体系，包括目录服务、存储服务、作业调度等，这里也会介绍这些服务的配置和维护。
        - Linux 系统运维的各项知识。
    - 相关任务：
        - 测试和更新系统。
        - 维护集群服务，保障集群稳定运行。
        - 优化集群架构，探索提升集群性能。

!!! bug "[软件运维](software/index.md)"

    - 内容：
        - 应用层面的运维工作，包括软件环境的管理、软件的安装和配置等。
        - Lmod、Spack 等软件包管理工具。
    - 相关任务：更新、测试和维护集群中的软件环境。

!!! tip "[可观测性](observability/index.md)"

    - 内容：新一代运维致力于构建可观测性体系，它能够让团队评估、监测和改进分布式 IT 系统的性能。相比传统的监测方法，它要有效得多。
    - 相关任务：配置和维护监控、日志、告警等系统。

</div>

## 运维工作概述

!!! quote

    - [运维体系的构建 - 信息化观察网](https://www.infoobs.com/article/20210121/44942.html)

下面是工业界对运维工作的介绍：

> 运维的基础工作通常是针对现有系统及项目的，例如服务器、各类云产品，正在运行的项目、监控、账号权限管控，项目上线等等，是宽泛而繁琐的，少有建设性的内容。
>
> 当我们接手一套新的系统，就有必要将它本身及周边进行完善。在大公司里有较为全面的运维体系，有桌面运维、网络运维、安全运维、研发运维、数据库运维以及系统运维或应用运维等专业团队，而更多的公司运维可能只有 1-2 个。以上的岗位工作都需要完成。
>
> 在接触新环境时，面对的是上任留下的坑，这比开发接手代码要更加严峻。交接的资料其实不应该只是账号密码、工作流程，工作注意事项，更重要的是操作维护文档，因为系统很少有简单的环境，即便有，也会存在一些微妙的项目逻辑关系，稍有不慎，就有可能酿成线上问题。现在大多都是微服务的结构，增加了系统维护的复杂性。
>
> 例如接手后领导要你部署使用 docker 部署一个 java 服务 , 从正式环境复制一个到测试环境，结果启动后出问题了，可能是启动参数与目前环境不匹配，可能是连接权限未放开，可能是启动后连接的是生产的数据库，如果程序启动后清空或者修改了一些历史数据，令人细思极恐。
>
> 这种问题很常见，就我目前就遇到不少，好多配置信息写的很模糊，项目与项目之间耦合度非常高，没准就牵扯到哪个系统了，牵一发而动全身，是关也不敢关，改也不敢改，作为一名运维工程师，我们居然会不敢动一个项目！所以要打造一个铁桶出来，这是一个创造性的过程，也是我们深入项目的过程。只有更深入的了解项目，才能更好的去维护项目。

对于超算队来说，运维工作的任务和面对的情况也差不多，不过没有这么严峻。毕竟我们从事的是研究不是生产，不需要保障极高的可用性。在我们自有的小集群上，我们可以**灵活地进行运维工作，进行各种各样的探索和创新**，不需要遵循严格的运维程序。

但是，我们也需要建立一套**自动化运维体系**，以便于更好地管理集群，提高运维效率，最终**让运维人员从繁琐的重复性工作中解放出来，更多地投入到创新性工作中**。

!!! note "超算队运维的任务"

    1. 熟练掌握 Linux 系统运维和 HPC 集群管理知识。
    2. 在线上线下比赛时帮助解决综合性问题。
    3. 维护自有集群，为比赛和训练提供稳定好用的环境。
    4. 维护托管在集群的服务器。
    5. 为队内成员日常使用集群提供支持。

!!! tip "如何做一个好的运维？"

    - 基础：
        - 对自己当前的环境和任何东西都应该非常清楚；
        - 要有监控，切实有用的可以发现问题的监控；
        - 任何东西都要有备份，可以用于快速恢复，也要做恢复演练；
    - 进阶
        - 针对系统做优化处理；
        - 针对工作流程做优化处理；

在运维工作中，我们总结了两点原则：

1. Keep It Simple and Stupid

    这是为了减少运维的人力成本。构建简单而实用的系统就能满足我们的需求，不需要为了高大上而高大上，不要在没有扩展的需求时使用 scale out 的方案。下面是一些例子：

    !!! example "要不要上 K8S？"

        我们可能永远都不会上 K8S，因为我们的集群规模太小，K8S 的复杂性和学习成本远远超过了我们的需求。

        > 笔者与 AAA 战队的同学聊天时了解到他们的运维趣事。他们队里有一位“传奇运维”，给机子部署了 K8S，结果升级不做备份不看文档，丢了某届校赛所有题目的附件，最终也没有找回来。这是一个很好的反面教材，说明了 K8S 的复杂性和学习成本。

        > 北大 HPCGAME 2025 使用 K8S 作为基础架构，结果运维困难。他们的结论是：
        >
        > **Distributed OS? No way! Do your shared memory research first!**

2. 避免重复造轮子

    作为学生，我们没有很多时间精力投入到运维工作中。在运维方面有大量工业界生产的轮子，我们应当尽可能利用已有的轮子。自己生产的轮子最后可能质量堪忧且难以持续维护。

    这里有一个例外，就是偏系统架构底层的东西（比如系统管理和部署工具）往往都必须造轮子，因为差异太大了，没有一个通用的方案。此外，如果需要实现的功能比较简单，自己造轮子练练手也未尝不可。

## 运维进展

超算队运维体系从 2024 年开始逐步建立。第一年我们完成了基础设施的改造，包括机房、网络、系统等方面的改进。第二年我们将进一步完善运维体系，包括建立更多的监控、日志、自动化等系统，提高运维效率和稳定性。
