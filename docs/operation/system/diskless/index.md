# 无盘系统

!!! abstract

    本文介绍我们选择无盘系统的原因。技术细节见子文档。

!!! quote

    - [Managing Cluster Software Packages - ADMIN Magazine](https://www.admin-magazine.com/HPC/Articles/Managing-Cluster-Software-Packages)

我们的目标是：

- 方便地管理几十台节点
- 避免节点间软件包、用户等环境不一致造成问题

这些问题有很多解决方案，比如集群管理有 Ansible Playbook，软件包有以下解决方案：

- **Image Based** – A node disk image is propagated out to nodes on boot. Different “rolls” (images) can be constructed for different packages.
- **NFS Root** – Each node boots and installs everything as NFS root except for things that change for each node (e.g., /etc, /var). This system can be run disk-less or disk-full.
- **RAM Disk** – A RAM disk is created on each node that holds a running system image. The RAM disk system can be created in hybrid mode, wherein some files are available via NFS, and it can run disk-less or disk-full.

经过查阅资料和案例调研，最后决定采用 **NFS Root** 的方式，这种方式有几个非常方便的用法：

- 我们只需要在 NFS Root 上进行配置、升级和维护，不需要操作每台机器。
- 新机器接入后，不需要手动安装配置，直接拥有和现有节点一致的环境。
- 外出比赛时，选取需要的 NFS Root 写几个一样的盘，顺便写上引导也可以。到赛场，用其他介质引导启动，获得所有环境一致的节点，不用再一台台装系统。

NFS Root 保证了各节点的系统内核、软件包（APT）一致。在此之上，我们**对根文件系统使用 OverlayFS**，使得节点拥有对根文件系统的完整权限，同时不会影响到其他节点，且系统易于恢复。
