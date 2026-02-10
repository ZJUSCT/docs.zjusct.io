---
tags:
  - 不完善
---

# 虚拟化平台：PVE

Proxmox Virtual Environment (PVE)

## 网络

自 PVE 8 开始，PVE 的网络基于 SDN 架构。自顶向下划分为：

- zone：独立的网络区域
    - 如果需要内置 DHCP 管理，应当在 Web 界面创建时勾选 Advanced 选择自动 DHCP。
- VNet：归属于 zone
    - 创建 VNet 后，对应的网络接口会被添加到所有节点上
- subnet：VNet 中的 IP 段
    - subnet 可以进行路由、源 NAT 等配置
    - 设置源 NAT 后，PVE 会在 `/etc/network/interfaces.d` 下的配置文件中添加 `post-up` 和 `post-down` 的 iptables 规则。

        !!! tip "但仅仅在对应接口配置 SNAT 往往是不够的，还需要允许从接口到 WAN 的双向转发。此外，如果需要从节点外访问，还需要在外部配置好路由。"

其他组件有：

- IPAM：IP 地址管理。一般使用内置的 PVE IPAM Plugin，可以配置到多个 zone。
- dnsmasq DHCP Plugin：用于在 zone 中提供 DHCP 服务，只要系统中安装了 dnsmasq 即可。
    - PVE 自动在 `/etc/dnsmasq.d/<zone>` 下创建配置文件，需要在 `/etc/dnsmasq.conf` 中包含这个目录，如果已有自定义配置文件需要注意冲突。
    - 虽然勾选的是“自动 DHCP“，但看配置文件创建的是 static only 的配置，也就是说不会自动分配 IP 地址，只会为已知主机分配固定 IP。可以在 IPAM 页面添加 DHCP Mapping。

        !!! bug

            但是现在好像有 bug，没有写入到 ether 文件中。IPAM 插件中相关的源码在 <https://github.com/proxmox/pve-network/blob/e0e0f4fa869578558bfe8fdf19217f451852ae7f/src/PVE/Network/SDN/Dhcp/Dnsmasq.pm#L52C5-L52C20>，待确认是否得到执行。

!!! tip "在 SDN 面板下进行的配置不会立刻生效，确认无误后回到 SDN 概览页面点击 Apply 才会生效。"
