---
tags:
  - 归档
---

# 网络信息服务：NIS

Network Information Service

!!! warning "archive"

    被 [LDAP](ldap.md) 取代。

!!! quote

    - [https://wiki.debian.org/BullseyeNis/](https://wiki.debian.org/BullseyeNis/)
    - [https://webmin.com/docs/modules/nis-client-and-server/](https://webmin.com/docs/modules/nis-client-and-server/)

## 概念

NIS 使用中心服务器管理网络中所有主机的账户、密码、UID、主目录和 Shell 等信息，提供 `/etc/passwd` 、 `/etc/group` 和 `/etc/hosts` 等 ASCII 文件信息。这些信息在服务器上存储为 DBM 数据库格式，收到请求时进行查找。

NIS 使用 RPC 协议。

NIS 以前被称为黄页（Yellow Page），在配置时你会看见 `yp` 就是它的缩写。这些信息也被称为映射（NIS map）。

NIS 环境中有主/从服务器和客户端三种类型的主机，从服务器维护主服务器的数据库副本，可以实现高可用和负载均衡。

- 广播方法：客户端发送广播，第一个回应的被绑定为服务器。
- 指定服务器方法：客户端维护服务器列表，依次尝试。

## Linux 中与用户账户相关的文件

- `/etc/shadow` ：存放加密的用户密码，只有 `root` 可以访问。
- `/etc/passwd` ：用户信息
- `/etc/group` ：用户组信息

## 安装

- `nis` 软件包包含 `rpcbind`、`ypbind` 、 `ypserv` 等所需的软件包。
- `libnss-nis`

## 主服务器配置

- 设置 NIS 域名： `/etc/defaultdomain`
- 主从服务器上都配置好 `/etc/hosts` ，写入所有其他服务器/客户端的 IP 地址，因为 NIS 不会使用 DNS

```bash
172.25.2.x NAS00
```

- （安全性，可选）设置 `/etc/ypserv.securenets` 和 `/etc/ypserv.conf` ，使得 NIS 服务器无法被外网访问。
- 启动服务：
    - `ypserv` 服务器
    - `yppasswdd` 密码
    - `ypxfrd` 传输映射数据
- NIS 使用 `/var/yp/Makefile` 更新映射。
- 启用广播模式：给 `rpcbind` 守护进程添加 `-r` 选项

```bash
echo "OPTIONS=-w -r" >>/etc/default/rpcbind
systemctl daemon-reload
```

## 客户端配置

- 设置 NIS 域名
- （可选）配置 `/etc/yp.conf` ：指定 NIS 服务器

```bash
ypserver xxx.xxx.xxx.xxx
```

- 启动 `ypbind` 服务
- 配置 `/etc/nsswitch.conf` ：

```bash
passwd:   compat
group:    compat
shadow:   compat
netgroup: nis
```

- 配置 `/etc/passwd` 、`/etc/shadow` 、 `/etc/group` ：在末尾加上一行

```bash
# passwd
+::::::
# shadow
+::::::::
# group
+:::
```

- （不建议）一般建议用 DNS 查找主机名。如果非要用 NIS，可以配置 `/etc/nsswitch.conf` ：

```bash
hosts:  files nis
```

## 从服务器配置

- 先按客户端配置
- 设置 `/etc/hosts` 、安全
- 配置 `/etc/default/nis` ：

```bash
NISSERVER=slave
```

> 该步疑似被弃用？需验证
> Again this is obsoleted by use of systemctl setup, and present there only for historical reasons and support the old sysv init script.

- 配置主服务器 `/var/yp/Makefile` ，让它知道有从服务器：

```bash
NOPUSH="false"
```

- 在主服务器上重建映射：

```bash
/usr/lib/yp/ypinit -m
```

- 在从服务器上启动服务 `ypserv` ，并配置主服务器：

```bash
systemctl enable ypserv.service
systemctl start ypserv.service
/usr/lib/yp/ypinit -s <name_of_your_master_nis_server_here>
```

- （可选）配置定时同步：主服务器更新时会推送，但若此时从服务器不在线，则可能错过推送。

```bash
systemctl enable ypxfr_1perday.timer
systemctl enable ypxfr_1perhour.timer
systemctl enable ypxfr_2perday.timer
systemctl start ypxfr_1perday.timer
systemctl start ypxfr_1perhour.timer
systemctl start ypxfr_2perday.timer
```

## 维护

对用户账户的修改都在主服务器上进行，修改后在 `/var/yp` 运行 `make` 使更改生效。

## 问题解决

- 客户端 `ypserv` 启动过程中卡死

可能是解析不出 `/etc/yp.conf` 中的服务器地址，检查服务器、网络是否正常。
